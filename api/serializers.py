from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import FormField, FormBody


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FormFieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormField
        fields = ['title', 'type', 'data', 'details', 'required']


class FormBodySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormBody
        fields = ['title', 'type', 'details', 'form_fields']
