from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from chat.models import Room, Message
from chat.forms import RegistrationForm
from django.contrib.auth import get_user_model



def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    """create room or retrieve it"""

    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })

@login_required
def group(request, group_name):
    """chat window view"""

    group = Room.objects.get(id=group_name)
    messages = group.message_set.all()
    return render(request, "partial/group-chat.html",{"messages":messages, "room_name":group_name,"name":group})

def notice(request):
    return render(request, "base.html")


def talk(request):
    """chat page view"""
    
    return render(request, "talk.html", {'messages': Message.objects.all(), 'groups':Room.objects.all()})
class RegistrationView(CreateView):
    template_name = "signup.html"
    model = get_user_model()
    success_url = reverse_lazy("login")

class SigninView(LoginView):
    next_page = "/chat/talk/"
    template_name = "signin.html"

    