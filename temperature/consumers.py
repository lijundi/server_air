from .models import *
from channels.generic.websocket import WebsocketConsumer
import json


class TempConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        info = json.loads(text_data)

        if "setpara" in info:
            temperature = Temperature.objects.all()[0]
            # temperature.mode = info['setpara']['mode']
            temperature.rate_l = info['setpara']['lowfan_change_temp']
            temperature.rate_m = info['setpara']['medfan_change_temp']
            temperature.rate_h = info['setpara']['highfan_change_temp']
            temperature.save()
            msg = json.dumps({'setpara': 'ok'})
        else:
            temperature = Temperature.objects.all()[0]
            temperature.serving = info['serving']
            if temperature.serving and info['fanSpeed'] == 2:
                temperature.temp = change_temp(temperature.rate_h, temperature.temp, info['tar_temp'])
            elif temperature.serving and info['fanSpeed'] == 1:
                temperature.temp = change_temp(temperature.rate_m, temperature.temp, info['tar_temp'])
            elif temperature.serving and info['fanSpeed'] == 0:
                temperature.temp = change_temp(temperature.rate_l, temperature.temp, info['tar_temp'])
            else:
                temperature.temp = change_temp(temperature.rate_default, temperature.temp, temperature.default_target_temp)

            t = temperature.temp  # 返回给客户端的当前温度
            temperature.save()  # 统一保存
            msg = json.dumps({'temp': t})

        self.send(msg)


def change_temp(rate, temp, tar_temp):
    if temp > tar_temp:
        temp -= rate
    elif temp < tar_temp:
        temp += rate
    return temp
