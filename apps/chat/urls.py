from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'', views.index, name='chat.index'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='chat.room'),
]
