from django.shortcuts import render
from django.contrib.auth.models import User, Group
from api.models import UserExtended
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserExtendedSerializer, GroupSerializer


# Create your views here.


def index(request):
    return render(request, 'index.html')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserExtended.objects.all().order_by('-middle_name')
    serializer_class = UserExtendedSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     username = self.request.query_params.get('username')
    #     queryset = User.objects.filter()


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



