from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Statuses(models.Model):
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True, null=True)

    class Meta:
        abstract = True


class Department(models.Model):
    name = models.CharField('Название', max_length=255, default='')
    is_regulator = models.BooleanField('Департамент утвердителей?', default=True)

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class User(AbstractUser):
    department = models.ForeignKey(Department, models.CASCADE, 'users', blank=True,
                                   null=True, verbose_name='Департамент')
    phone_number = models.CharField('Номер телефона', max_length=30)
    patronymic_name = models.CharField('Отчество', max_length=50)
    is_deleted = models.BooleanField('Удален ли пользователь', default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True


class Regulations(Statuses):
    name = models.CharField('Название регламента', max_length=255, default='')
    text = models.TextField('Текст регламента')
    version = models.PositiveSmallIntegerField('Версия регламентов')
    departments = models.ManyToManyField(Department, verbose_name='Департаменты')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'created_regulations',
                                   verbose_name='Кем создана', null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'updated_regulations',
                                   verbose_name='Кем обновлена', null=True)
    approved = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Одобрившие регламент',
                                      related_name='approved')

    class Meta:
        verbose_name = 'Регламент'
        verbose_name_plural = 'Регламенты'
        default_related_name = 'regulations'

    @property
    def status(self):
        if self.revisions.all():
            return "Ошибка"


class Revisions(Statuses):
    report = models.TextField('Сообщение по правке')
    paragraph = models.CharField('Абзац для правки', max_length=32)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                                   verbose_name='Кем создана', null=True)
    regulations = models.ForeignKey(Regulations, models.CASCADE, verbose_name='Регламент')

    class Meta:
        verbose_name = 'Правка'
        verbose_name_plural = 'Правки'
        default_related_name = 'revisions'
