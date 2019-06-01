from django.db import models


# Create your models here.
class Temperature(models.Model):
    # mode = models.IntegerField(default=0)  # 模式
    temp = models.FloatField(default=25.0)  # 当前室温
    # tar_temp = models.IntegerField(default=25)  # 目标温度
    default_target_temp = models.FloatField(default=25.0)  # 默认目标室温--用于回温程序
    serving = models.BooleanField(default=False)  # 服务状态
    rate_default = models.FloatField(default=1.0)  # 默认回温速率
    rate_h = models.FloatField(default=1.5)  # 高速风的变温速率
    rate_m = models.FloatField(default=1.0)  # 中速风的变温速率
    rate_l = models.FloatField(default=0.5)  # 低速风的变温速率

