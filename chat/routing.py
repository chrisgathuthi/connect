from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path("notification/", consumers.Notification.as_asgi()),
    re_path(r"talk/(?P<room_id>\w+)/$", consumers.TalkConsumer.as_asgi()),
]