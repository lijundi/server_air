# Generated by Django 2.1.3 on 2019-06-02 11:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20190525_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='channel_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='room',
            name='is_timer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='last_serving_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='workingparameter',
            name='fan',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='workingparameter',
            name='highfan_change_temp',
            field=models.FloatField(default=1.5),
        ),
        migrations.AddField(
            model_name='workingparameter',
            name='lowfan_change_temp',
            field=models.FloatField(default=0.5),
        ),
        migrations.AddField(
            model_name='workingparameter',
            name='medfan_change_temp',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='report',
            name='serving_duration',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='requestdetailrecords',
            name='fan_speed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='requestdetailrecords',
            name='request_duration',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='requestdetailrecords',
            name='request_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='current_temp',
            field=models.FloatField(default=25),
        ),
        migrations.AlterField(
            model_name='room',
            name='fan_speed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='serving_duration',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='target_temp',
            field=models.FloatField(default=25),
        ),
        migrations.AlterField(
            model_name='workingparameter',
            name='Temp_highLimit',
            field=models.FloatField(default=35),
        ),
        migrations.AlterField(
            model_name='workingparameter',
            name='Temp_lowLimit',
            field=models.FloatField(default=16),
        ),
        migrations.AlterField(
            model_name='workingparameter',
            name='default_TargetTemp',
            field=models.FloatField(default=25),
        ),
        migrations.AlterField(
            model_name='workingparameter',
            name='mode',
            field=models.IntegerField(default=0),
        ),
    ]