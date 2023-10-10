
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('meet/<str:room_name>/', views.room_view, name='chat-room'),
    path("base/", views.notice, name='notice'),
]