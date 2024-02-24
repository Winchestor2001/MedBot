import base64
import json
import os
import time

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from med_app.models import ChatStorage, Patient, Doctor, ChatMessage
from med_app.serializers import ChatPatientSerializer, ChatDoctorSerializer
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

        socket_data = await self.save_message_to_database(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": socket_data}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def save_message_to_database(self, text_data_json):
        message = text_data_json["message"]
        image = text_data_json.get("image_bytes", None)
        if image:
            _format, _img_str = image.split(';base64,')
            _name, ext = _format.split('/')
            image_content = base64.b64decode(_img_str)
            # storage = S3Boto3Storage()
            # image_path = f'media/{text_data_json["sender"]}/{text_data_json["receiver"]}/'
            image_filename = f'image_{int(time.time())}.png'
            with open('media/' + image_filename, 'wb') as f:
                f.write(image_content)
            # storage.save(image_filename, image_content)
            image = image_filename
        sender_id = text_data_json['sender']
        receiver_id = text_data_json['receiver']
        if text_data_json['type'] == 'patient':
            sender = ChatPatientSerializer(instance=Patient.objects.get(id=sender_id))
            receiver = ChatDoctorSerializer(instance=Doctor.objects.get(id=receiver_id))
        else:
            sender = ChatDoctorSerializer(instance=Doctor.objects.get(id=sender_id))
            receiver = ChatPatientSerializer(instance=Patient.objects.get(id=receiver_id))

        ch = ChatMessage.objects.create(
            chat=ChatStorage.objects.get(chat_code=self.room_name),
            sender=sender_id,
            receiver=receiver_id,
            message=message,
            image=image,
            type=text_data_json['type']
        )

        socket_data = {
            "sender": sender.data,
            "receiver": receiver.data,
            "message": text_data_json['message'],
            "image_bytes": ch.image.url if ch.image else None,
            "type": text_data_json['type']
        }

        return socket_data


class VideoConsumer(AsyncWebsocketConsumer):

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

    async def receive(self, text_data):
        message = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sdp.message',
                'message': message
            }
        )

    async def sdp_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
