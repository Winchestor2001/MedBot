import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

video_frames1 = []
video_frames2 = []


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

        await self.encode_and_save_webm()

    async def receive(self, text_data):
        message = text_data

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

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def video_record(self, video_bayt):
        video_bayt_json = json.loads(video_bayt)
        doctor_video_data = video_bayt_json['local'].encode('utf-8')
        patient_video_data = video_bayt_json['remote'].encode('utf-8')

        if doctor_video_data and patient_video_data:
            video_frames1.append(doctor_video_data)
            video_frames2.append(patient_video_data)

    async def encode_and_save_webm(self):
        if video_frames1:
            for d in video_frames1:
                with open(f"{self.room_name}.webm", "wb") as f:
                    f.write(d)

        video_frames1.clear()
