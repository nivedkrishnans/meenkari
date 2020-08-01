from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/lobby/<str:url_id>", consumers.LobbyConsumer),
            path("ws/play/<str:url_id>", consumers.GameConsumer),
        ])
    ),
})
