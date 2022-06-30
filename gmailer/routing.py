from django.urls import re_path

from gmailer.consumers import SocketAdapter

websocket_urlpatterns = [
    re_path(r'^ws/', SocketAdapter.as_asgi()),
]