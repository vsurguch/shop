# Generated by Django 2.1 on 2018-10-07 06:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20180922_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 9, 6, 5, 20, 768760, tzinfo=utc)),
        ),
    ]
