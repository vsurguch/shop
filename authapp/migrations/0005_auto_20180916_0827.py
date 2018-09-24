# Generated by Django 2.1 on 2018-09-16 15:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20180916_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuserprofile',
            name='photo_link',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 18, 15, 27, 23, 567639, tzinfo=utc)),
        ),
    ]
