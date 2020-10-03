import os

from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from xhtml2pdf import pisa

from api.models import Department, Regulations
from api.serializers import (UserInfoSerializer, GroupSerializer, DepartmentSerializer,
                             RegulationsSerializer)


# Create your views here.


def index(request):
    return render(request, 'index.html')


pisa.showLogging()


def dumpErrors(pdf, showLog=True):
    if pdf.err:
        print(pdf.err)


def html_to_pdf(request):
    # regulation_id = request.GET.get('id')
    # regulation = Regulations.objects.get(pk=regulation_id)
    regulation = """Hello <b>World</b><br/>"""
    output_filename = os.path.join('/home/zaysevkun/PycharmProjects/ReglamentsAPI(old)',
                                   'pdfs/regulation.pdf')
    result_file = open(output_filename, "w+b")

    pisa_status = pisa.CreatePDF(
        regulation,
        dest=result_file)
    result_file.close()
    return HttpResponse('ok')


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


class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-last_name')
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegulationsViewSet(viewsets.ModelViewSet):
    queryset = Regulations.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegulationsSerializer
