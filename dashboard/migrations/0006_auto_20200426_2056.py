# Generated by Django 3.0.5 on 2020-04-26 20:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20200426_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='beginning',
            field=models.DateField(default=datetime.datetime(2020, 4, 26, 20, 56, 44, 573465, tzinfo=utc)),
        ),
    ]