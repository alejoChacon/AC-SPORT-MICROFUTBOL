from django.urls import path
from .consumer import MainConsumer

websocket_urlpatterns = [
    path('ws/main/',MainConsumer.as_asgi()),
]