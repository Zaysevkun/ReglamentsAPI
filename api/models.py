from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Statuses(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'created_appeals',
                                   verbose_name='Кем создана', null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'updated_appeals',
                                   verbose_name='Кем обновлена', null=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True, blank=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Department(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class User(AbstractUser):
    POSITION_CHOICES = [
        ('employee', 'Составитель Регламента'),
        ('regulator', 'Утвердитель Регламента'),
        ('superuser', 'Суперюзер'),
    ]
    department = models.ForeignKey(Department, models.CASCADE, 'users', blank=True, null=True)
    phone_number = models.CharField('Номер телефона', max_length=30)
    position = models.CharField('Должность', max_length=50, choices=POSITION_CHOICES)
    patronymic_name = models.CharField('Отчество', max_length=50)
    is_deleted = models.BooleanField('Удален ли пользователь', default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True


class Regulations(models.Model):
    text = models.TextField('Текст регламента')
    version = models.PositiveSmallIntegerField('Версия регламентов')

    class Meta:
        verbose_name = 'Регламент'
        verbose_name_plural = 'Регламенты'
        default_related_name = 'regulations'


class Revisions(models.Model):
    report = models.TextField()

    class Meta:
        verbose_name = 'Правка'
        verbose_name_plural = 'Правки'
