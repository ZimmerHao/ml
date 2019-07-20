from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from libs.kubernetes.client import K8SClient


class LogConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("connect starting .........")
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("disconnect starting .........")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # Send message to room group
        lines = "sssssss"
        # k = K8SClient()
        # lines = k.get_logs("webapp-774dcf7d6f-r5v6r")
        print("................")
        print(lines)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': lines
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        lines = "sssssss"
        # k = K8SClient()
        # lines = k.get_logs("webapp-774dcf7d6f-r5v6r")
        # Send message to WebSocket
        print("................")
        print(lines)
        self.send(text_data=json.dumps({
            'message': lines
        }))
