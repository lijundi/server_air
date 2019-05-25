# Generated by Django 2.1.3 on 2019-05-24 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.IntegerField(default=25)),
                ('target_temp', models.IntegerField(default=25)),
                ('serving', models.BooleanField(default=False)),
                ('rate_default', models.IntegerField(default=1)),
                ('rate_h', models.IntegerField(default=3)),
                ('rate_m', models.IntegerField(default=2)),
                ('rate_l', models.IntegerField(default=1)),
                ('pre_change_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]