from django.contrib.auth.models import Group, User
from rest_framework import serializers

from api.consts import TEXT1_LABEL, TEXT2_LABEL, TEXT3_LABEL, TEXT4_LABEL, TEXT5_LABEL
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
        user_info = obj.users.all()
        if user_info:
            return UserInfoSerializer(user_info.first().user).data
        else:
            return {}


class RevisionsSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)

    class Meta:
        model = Revisions
        fields = ('id', 'report', 'paragraph', 'paragraph',
                  'created_by', 'regulation_part', 'created_at')


class Text1Serializer(serializers.ModelSerializer):
    label = TEXT1_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text1

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text1'),
                                   many=True).data


class Text2Serializer(serializers.ModelSerializer):
    label = TEXT2_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text2

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text2'),
                                   many=True).data


class Text3Serializer(serializers.ModelSerializer):
    label = TEXT3_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text3

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text3'),
                                   many=True).data


class Text4Serializer(serializers.ModelSerializer):
    label = TEXT4_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text4

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text4'),
                                   many=True).data


class Text5Serializer(serializers.ModelSerializer):
    label = TEXT5_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text5

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text5'),
                                   many=True).data


class LabelSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'comments')

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='label'),
                                   many=True).data


class PartsSerializer(serializers.ModelSerializer):
    text1 = Text1Serializer(source='*')
    text2 = Text2Serializer(source='*')
    text3 = Text3Serializer(source='*')
    text4 = Text4Serializer(source='*')
    text5 = Text5Serializer(source='*')
    label = LabelSerializer(source='*')

    class Meta:
        model = Regulations
        fields = ('text1', 'text2', 'text3', 'text4', 'text5', 'label')


class RegulationsSerializer(serializers.ModelSerializer):
    approved = UserInfoSerializer(many=True, read_only=True)
    created_by = UserInfoSerializer(read_only=True)
    updated_by = UserInfoSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    departments_users = serializers.SerializerMethodField()
    department_id = serializers.PrimaryKeyRelatedField(
        required=True, source='departments', write_only=True,
        queryset=Department.objects.all())
    parts = PartsSerializer(read_only=True, source='*')

    class Meta:
        model = Regulations
        fields = ('name', 'label', 'version', 'version_history_id', 'departments',
                  'department_id', 'created_at', 'updated_at', 'status', 'created_by', 'updated_by',
                  'approved', 'departments_users', 'parts')
        extra_kwargs = {
            'version': {'read_only': True},
            'version_history_id': {'read_only': True}
        }

    @staticmethod
    def get_departments_users(obj):
        return DepartmentsUsersSerializer(obj.departments.all(), many=True).data
