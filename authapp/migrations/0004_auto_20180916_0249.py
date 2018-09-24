# Generated by Django 2.1 on 2018-09-16 09:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20180916_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 9, 49, 56, 173280, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='myuserprofile',
            name='city',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]
