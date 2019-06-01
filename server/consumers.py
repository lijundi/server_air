from channels.generic.websocket import WebsocketConsumer
from server.interface import *
import json


class AirConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        info = json.loads(text_data)

        if "poweron" in info:
            dic = m_poweron(info['poweron']['room_id'], info['poweron']['cur_temp'], self.channel_name)
        elif "poweroff" in info:
            dic = m_poweroff(info['poweroff']['room_id'])
        elif "config" in info:
            dic = m_config(info['config']['room_id'], info['config']['fan'], info['config']['target_temp'])
        elif "temp_update" in info:
            dic = temp_update(info['temp_update']['room_id'], info['temp_update']['cur_temp'])
        else:
            dic = {}

        msg = json.dumps(dic)
        self.send(msg)
