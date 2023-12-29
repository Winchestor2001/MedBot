import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from med_app.utils import save_recorded_video


class VideoConsumer1(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"video_chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.encode_and_save_webm()

    async def receive(self, bytes_data):
        message = bytes_data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'video.message',
                'message': message
            }
        )
        await self.video_record(message)

    async def video_message(self, event):
        message = event['message']

        await self.send(bytes_data=message)

    async def video_record(self, video_bayt):
        current_direction = os.getcwd()
        with open(f"{current_direction}/media/{self.room_name}_1.webm", "ab") as f:
            f.write(video_bayt)

    async def encode_and_save_webm(self):
        save_recorded_video(
            f"{self.room_name}_1.webm", f"{self.room_name}_2.webm", f"recorded_{self.room_name}.webm"
        )


class VideoConsumer2(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"video_chat__{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, bytes_data):
        message = bytes_data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'video.message',
                'message': message
            }
        )
        await self.video_record(message)

    async def video_message(self, event):
        message = event['message']

        await self.send(bytes_data=message)

    async def video_record(self, video_bayt):
        current_direction = os.getcwd()
        with open(f"{current_direction}/media/{self.room_name}_2.webm", "ab") as f:
            f.write(video_bayt)
