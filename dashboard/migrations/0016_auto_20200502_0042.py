# Generated by Django 3.0.5 on 2020-05-02 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20200502_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='username',
            field=models.CharField(max_length=150),
        ),
    ]