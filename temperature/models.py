from django.db import models


# Create your models here.
class Temperature(models.Model):
    temp = models.IntegerField(default=25)  # 当前室温
    target_temp = models.IntegerField(default=25)  # 目标室温
    serving = models.BooleanField(default=False)  # 服务状态
    rate_default = models.IntegerField(default=1)  # 默认回温速率
    rate_h = models.IntegerField(default=3)  # 高速风的变温速率
    rate_m = models.IntegerField(default=2)  # 中速风的变温速率
    rate_l = models.IntegerField(default=1)  # 低速风的变温速率
    pre_change_date = models.DateTimeField()  # 保存上一次的变温时间
