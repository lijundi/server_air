from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from server.interface import *
from .models import *
import json


class AirConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        room_list = Room.objects.filter(channel_name=self.channel_name)
        for room in room_list:
            room.channel_name = ''
            room.save()
        pass

    def receive(self, text_data):
        info = json.loads(text_data)

        if "poweron" in info:
            wp = WorkingParameter.objects.all()[0]
            dic1 = {'setpara': {'mode': wp.mode,
                                'target_temp': wp.default_TargetTemp,
                                'highlimit_temp': wp.Temp_highLimit,
                                'lowlimit_temp': wp.Temp_lowLimit,
                                'highfan_change_temp': wp.highfan_change_temp,
                                'lowfan_change_temp': wp.lowfan_change_temp,
                                'medfan_change_temp': wp.medfan_change_temp,
                                'fan': wp.fan}}
            self.send(json.dumps(dic1))
            dic2 = m_poweron(info['poweron']['room_id'], info['poweron']['cur_temp'], self.channel_name)
            if dic2:  # 开机时室温温度与目标温度一致
                self.send(json.dumps(dic2))
                self.send(json.dumps({'finish': ''}))
            # else:
            #     dic3 = temp_update(info['poweron']['room_id'], info['poweron']['cur_temp'])
            #     if dic3:
            #         self.send(json.dumps(dic3))
        elif "poweroff" in info:
            dic = m_poweroff(info['poweroff']['room_id'])
            self.send(json.dumps(dic))
        elif "config" in info:
            self.send(json.dumps({'config': 'ok'}))
            m_config(info['config']['room_id'], info['config']['fan'], info['config']['target_temp'])
        elif "temp_update" in info:
            dic = temp_update(info['temp_update']['room_id'], info['temp_update']['cur_temp'])
            if dic:
                self.send(json.dumps(dic))
            # 更新温度时发费用
            dic2 = count_fee(info['temp_update']['room_id'])
            self.send(json.dumps(dic2))

    def chat_message(self, event):
        # 主动发送消息
        self.send(text_data=json.dumps(event['text']))
