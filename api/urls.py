from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'regulations', views.RegulationsViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'revisions', views.RevisionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', views.CustomAuthToken.as_view()),
    path('pdf/', views.html_to_pdf)
]
