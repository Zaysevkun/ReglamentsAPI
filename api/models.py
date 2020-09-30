from django.db import models
import uuid


# Create your models here.


class FormField(models.Model):
    FORM_TYPE_CHOICES = [('text', 'Текст'),
                         ('radio', 'Радио кнопка'),
                         ('dropdown', 'Выпадающий список'),
                         ('date', 'Поле даты'),
                         ('checkbox', 'Чекбокс')]

    title = models.CharField('Название поля', max_length=255)
    type = models.CharField('Тип поля', max_length=31, choices=FORM_TYPE_CHOICES)
    data = models.TextField('Тело формы', blank=True, null=True)  # for radio, dropdown
    details = models.CharField('Поясняющий текст', max_length=255, blank=True, null=True)
    required = models.BooleanField('обязательно ли поле', default=False)

    class Meta:
        verbose_name = 'Поле справки'
        verbose_name_plural = 'Поля справок'

    def data_as_list(self):
        return str(self.data).split('\n')

    def __str__(self):
        return self.title


class FormBody(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    details = models.CharField('Поясняющий текст для справки', max_length=255,
                               blank=True, null=True)
    form_fields = models.ManyToManyField(FormField, verbose_name='Поля справки',
                                         related_name='form_body')

    class Meta:
        default_related_name = 'form_bodies'
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'

    def __str__(self):
        return self.title
