"""
ASGI config for MicroFutbol project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicroFutbol.settings')

django_asgi_app = get_asgi_application()

from channels.routing import URLRouter,ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack

import Home.routing
import miequipo.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Home.routing.websocket_urlpatterns +
            miequipo.routing.websocket_urlpatterns      
        )
    )
})
