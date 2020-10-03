from django.contrib.auth.models import Group
from api.models import User, Department
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class UsersSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), write_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'position', 'department',
                  'department_id', 'first_name', 'patronymic_name', 'last_name', 'is_deleted')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
