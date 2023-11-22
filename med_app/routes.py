from django.urls import re_path
from med_app import consumers


websocket_urlpatterns = [
    re_path(r'ws/video/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
]
