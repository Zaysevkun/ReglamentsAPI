# Generated by Django 3.1.1 on 2020-10-04 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_additionaluserinfo_allow_send_info_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='revisions',
            name='default_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
