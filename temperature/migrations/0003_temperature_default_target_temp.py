# Generated by Django 2.1.3 on 2019-05-30 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temperature', '0002_auto_20190524_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='temperature',
            name='default_target_temp',
            field=models.IntegerField(default=25),
        ),
    ]