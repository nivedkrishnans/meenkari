# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/lobby/(?P<url_id>[-\w]+)", consumers.LobbyConsumer.as_asgi()),
    re_path(r"ws/play/(?P<url_id>[-\w]+)", consumers.GameConsumer.as_asgi()),
]