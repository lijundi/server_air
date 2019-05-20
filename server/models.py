from django.db import models


# Create your models here.
# 基类
class Basic(models.Model):
    fan_speed = models.IntegerField()  # 0:低速风 1:中速风 2:高速风
    fee_rate = models.FloatField()
    fee = models.FloatField()

    class Meta:
        abstract = True


# 房间类
class Room(Basic):
    room_id = models.IntegerField(primary_key=True)
    state_working = models.BooleanField()
    state_serving = models.BooleanField()
    state_waiting = models.BooleanField()
    current_temp = models.IntegerField()
    target_temp = models.IntegerField()
    serving_duration = models.IntegerField()


# 详单类
class RequestDetailRecords(Basic):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    request_time = models.DateField()
    request_duration = models.IntegerField()


# 周报类
class Report(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    times_of_on_and_off = models.IntegerField(default=0)
    serving_duration = models.IntegerField(default=0)
    total_Fee = models.FloatField(default=0)
    times_of_dispatch = models.IntegerField(default=0)
    number_of_RDR = models.IntegerField(default=0)
    times_of_changeTemp = models.IntegerField(default=0)
    times_of_changeFanSpeed = models.IntegerField(default=0)


# 空调工作参数
class WorkingParameter(models.Model):
    mode = models.IntegerField()  # 0:制冷 1:制热
    Temp_highLimit = models.IntegerField()
    Temp_lowLimit = models.IntegerField()
    default_TargetTemp = models.IntegerField()
    FeeRate_H = models.FloatField()
    FeeRate_M = models.FloatField()
    FeeRate_L = models.FloatField()
