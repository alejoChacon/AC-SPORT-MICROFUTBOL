from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from Torneo.models import Equipo
from Home.models import NotificacionSolicitud

@database_sync_to_async
def obtener_datos_equipos(pk):
    try:
        equipo = Equipo.objects.get(pk=pk)
        return {
            'equipo_pk':pk,
            'nombre':equipo.nombre,
            'capitan_pk':equipo.capitan.pk,
            'capitan':equipo.capitan.get_full_name()
        }
    except Equipo.DoesNotExist:
        print('Equipo No existe')
    except Exception as e:
        print('Error en BD: ',str(e))

class ConsumerMiEquipo(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        await self.accept()
        print('Conexion establecida para el apartado mi equipo')
    
    async def disconnect(self, code):
        print('Desconectado!!!')
        return await super().disconnect(code)
    
    async def receive(self, text_data = None):
        text = json.loads(text_data)
        equipo_pk = text.get('equipo_id')
        equipo = await obtener_datos_equipos(equipo_pk)
        if equipo:
            id_notificacion = await self.save_notification(equipo)
            await self.channel_layer.group_send(
                f"user_{equipo['capitan_pk']}",
                {
                    'type':'send_notification',
                    'equipo_pk':equipo['equipo_pk'],
                    'equipo':equipo['nombre'],
                    'capitan':equipo['capitan'],
                    'jugador_send_request':self.user.get_full_name(),
                    'jugador_send_pk':self.user.pk,
                    'notificacion_pk':id_notificacion,
                    'notificacion':True
                }
            )
        else:
            print('No se pudo enviar la notificacion: Equipo no encontrado')
    
    @database_sync_to_async
    def save_notification(self,equipo):
        print(equipo)
        try:
            notificacion = NotificacionSolicitud.objects.create(
                receptor_id = equipo['capitan_pk'],
                remitente = self.user,
                equipo_id = equipo['equipo_pk']
            )
            return notificacion.pk
        except Exception as e:
            print("Hubo un error: ",str(e))