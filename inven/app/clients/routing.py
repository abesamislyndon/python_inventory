from django.urls import re_path
from .consumers import MessageBoardConsumer

websocket_urlpatterns = [
    re_path(r'^ws/message_board/(?P<client_url>[\w-]+)/$', MessageBoardConsumer.as_asgi()),
]
