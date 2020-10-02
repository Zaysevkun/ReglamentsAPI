from django.db import models
from django.contrib.auth.models import User as BasicUser
import uuid


# Create your models here.


class User(models.Model):
    user = models.OneToOneField(BasicUser, on_delete=models.CASCADE)
    phone_number = models.CharField('номер телефона', max_length=20, default=False)

