from django.urls import path
from .consumer import ConsumerMiEquipo

websocket_urlpatterns = [
    path('ws/myteam/',ConsumerMiEquipo.as_asgi()),
]