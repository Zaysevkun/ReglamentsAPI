from django.contrib.auth.models import Group, User
from rest_framework import serializers

from api.models import Department, Regulations, AdditionalUserInfo


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


class RegulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regulations
        field = ('name',)
