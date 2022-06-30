from django.conf.urls import url

from gmailer.consumers import SocketAdapter

websocket_urlpatterns = [
    url(r'^ws/', SocketAdapter.as_asgi()),
]