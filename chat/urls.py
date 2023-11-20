
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('meet/<str:room_name>/', views.room_view, name='chat-room'),
    path("base/", views.notice, name='notice'),
    path("talk/", views.talk, name='talk'),
    path("group/<str:group_name>/",views.group, name='group'),
    path("signup/", views.RegistrationView.as_view(), name='signup'),
    path("login/", views.SigninView.as_view(), name='login'),
]