# myapp/routing.py

from django.urls import path
from . consumers import MessageBoardConsumer

websocket_urlpatterns = [
    path('ws/message_board/', MessageBoardConsumer.as_asgi()),
]
