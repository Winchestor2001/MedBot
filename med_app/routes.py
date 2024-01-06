from django.urls import re_path
from med_app import consumers


websocket_urlpatterns = [
    re_path(r'ws/meet/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
