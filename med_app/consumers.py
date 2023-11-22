# chat/consumers.py
import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"video_chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Получение данных видео в виде base64-encoded строки
        video_data = json.loads(text_data)['video']

        # Декодирование base64 в бинарные данные
        video_bytes = base64.b64decode(video_data)

        # Отправка бинарных данных всем подключенным клиентам в комнате
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'video.message',
                'video': video_bytes
            }
        )

    # Receive video message from room group
    async def video_message(self, event):
        video_bytes = event['video']

        # Отправка бинарных данных видео на WebSocket
        await self.send(text_data=json.dumps({
            'video': base64.b64encode(video_bytes).decode('utf-8')
        }))
