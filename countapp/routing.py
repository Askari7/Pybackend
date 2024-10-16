from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import consumers  # Use relative import for consumers
from django.urls import path

websocket_urlpatterns = [
    path("ws/api/get-data/", consumers.MyConsumer.as_asgi()),  # WebSocket URL
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
