# Generated by Django 3.1.1 on 2020-10-03 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Департамент',
                'verbose_name_plural': 'Департаменты',
            },
        ),
        migrations.CreateModel(
            name='Regulations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст регламента')),
                ('version', models.PositiveSmallIntegerField(verbose_name='Версия регламентов')),
            ],
            options={
                'verbose_name': 'Регламент',
                'verbose_name_plural': 'Регламенты',
                'default_related_name': 'regulations',
            },
        ),
        migrations.CreateModel(
            name='Revisions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.TextField()),
            ],
            options={
                'verbose_name': 'Правка',
                'verbose_name_plural': 'Правки',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='api.department'),
        ),
    ]
