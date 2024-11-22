"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack  # type: ignore
from channels.routing import ProtocolTypeRouter, URLRouter  # type: ignore
from django.core.asgi import get_asgi_application  # type: ignore
from django.urls import path  # type: ignore

from room.consumer import RoomConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/room/", RoomConsumer.as_asgi()),
                ]
            )
        ),
    }
)
