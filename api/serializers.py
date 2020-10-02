from django.contrib.auth.models import User, Group
from api.models import UserExtended
from rest_framework import serializers


class UserExtendedSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = UserExtended
        fields = ['username', 'email', 'phone_number', 'position',
                  'first_name', 'middle_name', 'last_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)

        profile = UserExtended.objects.create(user=user, **validated_data)
        return profile


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
