# Generated by Django 3.0.5 on 2020-04-28 00:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20200428_0016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboard',
            name='status',
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='beginning',
            field=models.DateField(default=datetime.datetime(2020, 4, 28, 0, 36, 26, 571010, tzinfo=utc)),
        ),
    ]