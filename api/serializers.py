from django.contrib.auth.models import Group, User
from rest_framework import serializers

from api.models import Department, Regulations, AdditionalUserInfo, Revisions


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class UserInfoSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True, source='info.department')
    department_id = serializers.PrimaryKeyRelatedField(
        required=True, source='department', write_only=True,
        queryset=Department.objects.all())
    password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(source='info.phone_number')
    patronymic_name = serializers.CharField(source='info.patronymic_name', required=False)
    is_deleted = serializers.CharField(source='info.is_deleted', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone_number', 'department',
                  'department_id', 'first_name', 'patronymic_name', 'last_name', 'is_deleted',
                  'is_superuser')

    def create(self, validated_data):
        info = validated_data.pop('info')
        department = validated_data.pop('department')
        info['department_id'] = department.id
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password, **validated_data)
        info = AdditionalUserInfo.objects.create(**info)
        info.user = user
        info.save()
        return User.objects.get(id=user.id)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DepartmentsUsersSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('name', 'user')

    @staticmethod
    def get_user(obj):
        return UserInfoSerializer(obj.users.all()[0].user).data


class RegulationsSerializer(serializers.ModelSerializer):
    approved = UserInfoSerializer(many=True, read_only=True)
    created_by = UserInfoSerializer(read_only=True)
    updated_by = UserInfoSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    departments_users = serializers.SerializerMethodField()
    department_id = serializers.PrimaryKeyRelatedField(
        required=True, source='departments', write_only=True,
        queryset=Department.objects.all())

    class Meta:
        model = Regulations
        fields = ('name', 'label', 'text', 'version', 'version_history_id', 'departments',
                  'department_id', 'created_at', 'updated_at', 'status', 'created_by', 'updated_by',
                  'approved', 'departments_users')
        extra_kwargs = {
            'version': {'read_only': True},
            'version_history_id': {'read_only': True}
        }

    @staticmethod
    def get_departments_users(obj):
        return DepartmentsUsersSerializer(obj.departments.all(), many=True).data
