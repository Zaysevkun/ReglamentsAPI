from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.models import UserExtended
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from api.serializers import UserExtendedSerializer, GroupSerializer


# Create your views here.


def index(request):
    return render(request, 'index.html')


# def whoami(request):
#     if request:
#         id = request.user.id
#         return JsonResponse({'id': id})
#     return JsonResponse({'detail': 'You are not authorized.'})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
        })


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
