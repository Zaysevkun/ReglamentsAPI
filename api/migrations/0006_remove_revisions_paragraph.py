# Generated by Django 3.1.1 on 2020-10-03 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201003_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revisions',
            name='paragraph',
        ),
    ]