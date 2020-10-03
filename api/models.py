from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models, transaction
from django.db.models import Max


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

    def __str__(self):
        return self.name


class AdditionalUserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE,
                                related_name='info',
                                blank=True, null=True)
    department = models.ForeignKey(Department, models.CASCADE, 'users', blank=True,
                                   null=True, verbose_name='Департамент')
    phone_number = models.CharField('Номер телефона', max_length=30)
    patronymic_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    is_deleted = models.BooleanField('Удален ли пользователь', default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True


class Regulations(Statuses):
    name = models.CharField('Название регламента', max_length=255, default='')

    label = models.TextField('Заголовок', default='')
    text1 = models.TextField('Текст 1 раздела', default='')
    text2 = models.TextField('Текст 2 раздела', default='')
    text3 = models.TextField('Текст 3 раздела', default='')
    text4 = models.TextField('Текст 4 раздела', default='')
    text5 = models.TextField('Текст 5 раздела', default='')

    version = models.PositiveSmallIntegerField('Версия регламентов', blank=True, null=True,
                                               default=None)
    version_history_id = models.PositiveBigIntegerField('Номер истории',
                                                        null=True, blank=True, default=None)
    departments = models.ManyToManyField(Department, verbose_name='Департаменты')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'created_regulations',
                                   verbose_name='Кем создана', blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'updated_regulations',
                                   verbose_name='Кем обновлена', blank=True, null=True)
    approved = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Одобрившие регламент',
                                      related_name='approved', blank=True)

    class Meta:
        verbose_name = 'Регламент'
        verbose_name_plural = 'Регламенты'
        default_related_name = 'regulations'

    @property
    def status(self):
        departments = self.departments.all()
        if not departments:
            return "Создание"
        revisions = self.revisions.all().filter(is_marked_solved=False)
        if revisions:
            return "Ошибка"
        approved = self.approved.all()
        if approved.count() < departments.count():
            return "На согласовании"
        if not approved.count() < departments.count():
            return "Согласован"
        return "В работе"

    def combine(self):
        label = '<h3>' + self.label + '</h3>'
        text1 = self.text1
        text2 = self.text2
        text3 = self.text3
        text4 = self.text4
        text5 = self.text5
        regulation = label + text1 + text2 + text3 + text4 + text5
        return regulation

    def identify_version(self, previous_history_id=None, previous_version=None):
        with transaction.atomic():
            if not previous_history_id:
                last_version_history_id = Regulations.objects.aggregate(
                    Max('version_history_id'))['version_history_id__max']
                if not last_version_history_id:
                    self.version_history_id = 1
                else:
                    self.version_history_id = last_version_history_id + 1
                self.version = 1
            elif previous_history_id and previous_version:
                self.version_history_id = previous_history_id
                self.version = previous_version + 1
            self.save()


class Revisions(Statuses):
    REGULATIONS_PART_CHOICES = [
        ('text1', 'text1'),
        ('text2', 'text2'),
        ('text3', 'text3'),
        ('text4', 'text4'),
        ('text5', 'text5'),
        ('label', 'label')
    ]
    report = models.TextField('Сообщение по правке')
    secret_id = models.PositiveSmallIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                                   verbose_name='Кем создана', null=True)
    regulations = models.ForeignKey(Regulations, models.CASCADE, verbose_name='Регламент')
    regulation_part = models.CharField(max_length=32,
                                       choices=REGULATIONS_PART_CHOICES,
                                       default='text1')
    html_selection = models.TextField('Выделенный текст для правки', blank=True, null=True)
    is_marked_solved = models.BooleanField('Отмечен ли как решенный', default=False)

    class Meta:
        verbose_name = 'Правка'
        verbose_name_plural = 'Правки'
        default_related_name = 'revisions'


class Applications(models.Model):
    app_file = models.FileField('Файл приложения', max_length=5000)
    regulations = models.ForeignKey(Regulations, models.CASCADE, verbose_name='Регламент')

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'
        default_related_name = 'applications'
