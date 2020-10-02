from django.db import models
from django.contrib.auth.models import User as BasicUser
import uuid


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserExtended(models.Model):
    POSITION_CHOICES = [
        ('employee', 'Составитель Регламента'),
        ('regulator', 'Утвердитель Регламента'),
        ('superuser', 'Суперюзер'),
    ]

    user = models.OneToOneField(BasicUser, on_delete=models.CASCADE)
    phone_number = models.CharField('Номер телефона', max_length=20, default=False)
    position = models.CharField('Должность', max_length=50)
    first_name = models.CharField('Имя', max_length=50)
    middle_name = models.CharField('Фамилия', max_length=50)
    last_name = models.CharField('Отчество', max_length=50, default=False)

    # @receiver(post_save, sender=BasicUser)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         UserExtended.objects.create(user=instance)
    #
    # @receiver(post_save, sender=BasicUser)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.UserExtended.save()


