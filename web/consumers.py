from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from libs.kubernetes.client import K8SClient
import time


class LogConsumer(WebsocketConsumer):

    def connect(self):
        self.pod_name = self.scope['url_route']['kwargs']['pod_name']
        self.group_name = 'pod_log_%s' % self.pod_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'show_log',
                'message': message
            }
        )

    # Receive message from room group
    def show_log(self, event):
        message = event['message']
        # Send message to WebSocket
        pod_name = self.pod_name
        k = K8SClient()
        while True:
            time.sleep(1)
            lines = k.get_logs(pod_name, "default", since_seconds=1)
            self.send(text_data=json.dumps({
                'message': lines
            }))
