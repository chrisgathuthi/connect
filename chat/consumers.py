
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template
from .models import Room, Message, User

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope["user"]

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # user joined
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))

        if self.user.is_authenticated:
            # send the join event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            self.room.online.add(self.user)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )
        
        if self.user.is_authenticated:
            # send the leave event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )
            self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        if self.user.is_authenticated:
            return
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username
            }
        )

        Message.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        print(event)
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))


class Notification(WebsocketConsumer):

    def connect(self):
        self.group_name = "user-notification"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        self.group_name = "user-notification"
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )
        
    
    def user_joined(self, event):
        print(event)
        # self.send(text_data=event["text"])
        html = get_template("notification.html").render(context={'room': event["text"]})
        self.send(text_data=html)


class TalkConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None
        self.group_name = None
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'chat_{self.room}'
        self.room = Room.objects.get(id=self.room_name)
        self.user = self.scope["user"]

        # accept connection
        self.accept()

        # join the room/group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        # user joined notification
        html = get_template("partial/join.html").render(context={"user":self.user})
        self.send(text_data=html)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
        html = get_template("partial/leave.html").render(context={"user":self.user})
        self.send(
            text_data=html
        )
        self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        room = Room.objects.get(id=self.room_name)
        Message.objects.create(user=self.user, room=room, content=text_data_json['message'])

        html = get_template("chats.html").render(context={'messages': room.message_set.all()})
        self.send(text_data=html)