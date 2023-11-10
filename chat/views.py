from django.shortcuts import render

from chat.models import Room, Message


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })


def notice(request):
    return render(request, "base.html")


def talk(request):
    return render(request, "talk.html", {'messages': Message.objects.all(), 'groups':Room.objects.all()})