from django.db import models
from django.utils import timezone

# Create your models here.
# 基类

class Basic(models.Model):
    fan_speed = models.IntegerField(default=0)  # 0:低速风 1:中速风 2:高速风
    fee_rate = models.FloatField(default=1)
    fee = models.FloatField(default=0)

    class Meta:
        abstract = True


# 房间类
class Room(Basic):
    room_id = models.IntegerField(primary_key=True)
    state_working = models.BooleanField(default=False)
    state_serving = models.BooleanField(default=False)
    state_waiting = models.BooleanField(default=False)
    current_temp = models.FloatField(default=25)
    target_temp = models.FloatField(default=25)
    serving_duration = models.FloatField(default=0)
    channel_name = models.CharField(max_length=100, default='')
    last_serving_time = models.DateTimeField(default=timezone.now)
    init_cur_temp = models.FloatField(default=25)
    is_timer = models.BooleanField(default=False)
    for_timer_weight = models.FloatField(default=0)  # 时长-风速*10000


# 详单类
class RequestDetailRecords(Basic):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    request_time = models.DateTimeField()
    request_duration = models.FloatField()


# 周报类
class Report(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    times_of_on_and_off = models.IntegerField(default=0)
    serving_duration = models.FloatField(default=0)
    total_Fee = models.FloatField(default=0)
    times_of_dispatch = models.IntegerField(default=0)
    number_of_RDR = models.IntegerField(default=0)
    times_of_changeTemp = models.IntegerField(default=0)
    times_of_changeFanSpeed = models.IntegerField(default=0)


# 空调工作参数
class WorkingParameter(models.Model):
    mode = models.IntegerField(default=0)  # 0:制冷 1:制热
    Temp_highLimit = models.FloatField(default=35)
    Temp_lowLimit = models.FloatField(default=16)
    default_TargetTemp = models.FloatField(default=25)
    FeeRate_H = models.FloatField()
    FeeRate_M = models.FloatField()
    FeeRate_L = models.FloatField()
    highfan_change_temp = models.FloatField(default=1.5)
    lowfan_change_temp = models.FloatField(default=0.5)
    medfan_change_temp = models.FloatField(default=1.0)
    fan = models.IntegerField(default=0)
