# Generated by Django 2.1 on 2018-09-23 06:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20180919_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 25, 6, 41, 18, 268362, tzinfo=utc)),
        ),
    ]
