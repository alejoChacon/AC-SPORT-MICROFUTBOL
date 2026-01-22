from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class MainConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user = self.scope['user']
        self.name_channel = f"user_{self.user.pk}"
        await self.channel_layer.group_add(
            self.name_channel,
            self.channel_name
        )
        await self.accept()
        print('Conexion Establecida')
    
    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.name_channel,
            self.channel_name
        )
        print('Se ha desconectado')
    
    async def receive(self, text_data = None):
        text = json.loads(text_data)
        await self.send_notification(text)
        print('Mensaje Recibido: ',text)
        
    
    async def send_notification(self,event):
        notificacion = event['notificacion']
        if notificacion:
            data_to_send = {
                'equipo_pk':event['equipo_pk'],
                'equipo':event['equipo'],
                'capitan':event['capitan'],
                'jugador_send_request': event['jugador_send_request'],
                'jugador_send_pk': event['jugador_send_pk'],
                'notificacion_pk': event['notificacion_pk']
            }
            await self.send(json.dumps(data_to_send))