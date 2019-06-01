from .models import *
from channels.generic.websocket import WebsocketConsumer
import json


class AirConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        info = json.loads(text_data)

        if "poweron" in info:
            print(1)
        elif "poweroff" in info:
            print(1)
        elif "config" in info:
            print(1)
        elif "temp_update" in info:
            print(1)

        msg = json.dumps({})
        self.send(msg)
