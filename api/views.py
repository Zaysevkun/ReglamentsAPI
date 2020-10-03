import os
import io

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

from ReglamentsAPI.settings import STATIC_ROOT
from api.models import Department, Regulations, Revisions
from api.serializers import (UserInfoSerializer, GroupSerializer, DepartmentSerializer,
                             RegulationsSerializer, RevisionsSerializer)


# Create your views here.


def index(request):
    return render(request, 'index.html')


pisa.showLogging()


def dumpErrors(pdf, showLog=True):
    if pdf.err:
        print(pdf.err)


def html_to_pdf(request):
    regulation_id = request.GET.get('id')
    regulation = Regulations.objects.get(pk=regulation_id)
    regulation_full = regulation.combine()
    font_path = os.path.join(STATIC_ROOT, 'pdf/fonts/times-new-roman.ttf')
    html_head = """meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Моя первая страничка</title>
<style type="text/css">
@font-face {
font-family: Arial;
src: url(""" + font_path + """);
}
div { font-family: arial; }
</style>"""
    regulation_full = html_head + regulation_full
    output_filename = os.path.join(STATIC_ROOT,
                                   'pdf/regulation.pdf')
    result_file = open(output_filename, "w+b")

    pisa_status = pisa.CreatePDF(
        regulation_full.encode("UTF-8"),
        dest=result_file, encoding='UTF-8')
    result_file = io.open(output_filename, encoding="utf-8")
    result_file.close()
    return HttpResponse(pisa_status.err)


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

    def retrieve(self, request, *args, **kwargs):
        regulation = self.get_object()
        version_history_id = regulation.version_history_id
        if not version_history_id:
            serializer_data = [self.get_serializer(regulation).data]
        else:
            regulations = (self.queryset
                           .filter(version_history_id=version_history_id)
                           .order_by('-created_at'))
            serializer_data = self.get_serializer(regulations, many=True).data
        return Response(serializer_data)


class RevisionsViewSet(viewsets.ModelViewSet):
    queryset = Revisions.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RevisionsSerializer
