"""
ASGI config for game project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from my_app.consumers import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tictactoe.settings")

#handle HTTP requests.
application = get_asgi_application()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    #URLRouter used to map WebSocket URLs to consumers
    "websocket": URLRouter([
        path("ws/game/<int:id>/<int:playerId>/", MyappConsumer.as_asgi()) #as_asgi() method is used to convert the consumer class to an ASGI application
    ])
})
