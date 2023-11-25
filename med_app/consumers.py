import json
from channels.generic.websocket import AsyncWebsocketConsumer


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
        text_data_json = json.loads(text_data)
        data = text_data_json['data']
        command = data['command']
        pre_data = {
            'type': 'send.sdp',
            "data": {}
        }
        if command == 'join':
            pre_data['data'] = {"peer-joined": {"data": data['data']}}

        elif command == 'leave':
            pre_data['data'] = {"leave": {"data": data['data']}}

        await self.channel_layer.group_send(
            self.room_group_name,
            pre_data
        )

    async def send_sdp(self, event):
        print(event)
        receive = event['data']
        await self.send(text_data=json.dumps(receive))

    # async def chat_message(self, event):
    #     message = event['message']
    #
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
