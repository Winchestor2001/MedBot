import base64
import json
import os
import time

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from med_app.models import ChatStorage, Patient, Doctor
from med_app.utils import save_recorded_video
from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage


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

    async def receive(self, bytes_data):
        message = bytes_data

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'video.message',
        #         'message': message
        #     }
        # )
        await self.video_record(message)

    async def video_message(self, event):
        message = event['message']

        await self.send(bytes_data=message)

    async def video_record(self, video_bayt):
        current_direction = os.getcwd()
        with open(f"{current_direction}/media/{self.room_name}_1.webm", "ab") as f:
            f.write(video_bayt)


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

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'video.message',
        #         'message': message
        #     }
        # )
        await self.video_record(message)

    async def video_message(self, event):
        message = event['message']

        await self.send(bytes_data=message)

    async def video_record(self, video_bayt):
        current_direction = os.getcwd()
        with open(f"{current_direction}/media/{self.room_name}_2.webm", "ab") as f:
            f.write(video_bayt)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_count = 0

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.users_count += 1
        await self.accept()

    async def disconnect(self, close_code):
        self.users_count -= 1
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await self.save_message_to_database(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": text_data_json}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def save_message_to_database(self, text_data_json):
        message = text_data_json["message"]
        image = text_data_json.get("image_bytes", None)
        if image:
            image_content = ContentFile(base64.b64decode(image), name='image.png')
            storage = S3Boto3Storage()
            image_path = f'media/{text_data_json["patient"]}/{text_data_json["doctor"]}/'
            image_filename = f'{image_path}image_{time.time()}.png'
            storage.save(image_filename, image_content)
            image = image_filename

        ChatStorage.objects.create(
            patient=Patient.objects.get(id=text_data_json['patient']),
            doctor=Doctor.objects.get(id=text_data_json['doctor']),
            message=message,
            image=image
        )
