from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/live/", consumers.LiveConsumer),
            path("ws/lobby/<str:url_id>", consumers.LobbyConsumer),
        ])
    ),
})
