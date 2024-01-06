from django.urls import re_path
from med_app import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/meeting-doctor/(?P<room_name>\w+)/$', consumers.VideoConsumer1.as_asgi()),
    re_path(r'ws/meeting-patient/(?P<room_name>\w+)/$', consumers.VideoConsumer2.as_asgi()),
]
