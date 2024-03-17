from django.urls import path
from . import views
from .views import (
    my_view,
    user_list,
    conversation_list,
    chat_room_detail,
    create_chat_room,
    create_user,
    get_updates,
    delete_message,
    my_login_view,
    send_message,
    logout_user
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # utilisé dans my_view.html
    path('', my_view, name='my_view'),

    # utilisé dans user_list.html
    path('users/', user_list, name='user_list'),

    # utilisé dans conversation_list.html
    path('conversations/', conversation_list, name='conversation_list'),

    # utilisé dans create_chat_room.html
    path('create_chat_room/', create_chat_room, name='create_chat_room'),

    # utilisé dans create_user.html
    path('create_user/', create_user, name='create_user'),

    # utilisé dans chat_room_detail.html
    path('chat_room_detail/<int:room_id>/', views.chat_room_detail, name='chat_room_detail'),    path('get_updates/', get_updates, name='get_updates'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('send_message/', send_message, name='send_message'),

    # utilisé dans login.html
    path('login/', my_login_view, name='my_login_view'),

    # utilisé dans plusieurs fichiers
    path('logout/', logout_user, name='logout'),
]
