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
        accion = text.get('informacion',)
        equipo_pk = text.get('equipo_id')
        equipo = await obtener_datos_equipos(equipo_pk)
        if accion == 'capitan':
            if await self.cantidadJugadores(self.user) >= 10:
                data_to_send = {'error':"No puedes enviar más solicitudes si tiene el cupo lleno en tu equipo"}
                await self.send(json.dumps(data_to_send))
                print('Error: equipo no puede enviar más solicitudes si tiene el cupo lleno')
                return
            self.receptorId = text.get('jugador_id',)
            id_notification = await self.save_notification(equipo)
            await self.channel_layer.group_send(
                f'user_{self.receptorId}',
                {
                    'type': 'send_notification',
                    'equipo_pk': equipo['equipo_pk'],
                    'equipo': equipo['nombre'],
                    'capitan': equipo['capitan'],
                    'capitan_pk': equipo['capitan_pk'],
                    'jugador_id': self.receptorId,
                    'notificacion_pk': id_notification,
                    'notificacion': True,
                    'informacion': 'capitan'
                }
            ) 
        elif accion == 'jugador':        
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
                        'notificacion':True,
                        'informacion': 'jugador'
                    }
                )
            else:
                print('No se pudo enviar la notificacion: Equipo no encontrado')
    
    @database_sync_to_async
    def save_notification(self,equipo):
        try:
            print(self.user.get_full_name())
            if equipo['capitan_pk'] == self.user.pk:
                notificacion = NotificacionSolicitud.objects.create(
                    receptor_id = self.receptorId,
                    remitente = self.user,
                    equipo_id = equipo['equipo_pk'],
                    informacion = 'capitan' #Quiere decir que está accion la realizó el capitan, El capitan envío solicitud de unirse al equipo
                )
                return notificacion.pk
            else:
                notificacion = NotificacionSolicitud.objects.create(
                    receptor_id = equipo['capitan_pk'],
                    remitente = self.user,
                    equipo_id = equipo['equipo_pk'],
                    informacion = 'jugador' #QUiere decir que esta accion la realizó el jugador, El jugador solicitó al capitan del equipo que lo acepte en su equipo.
                )
                return notificacion.pk
        except Exception as e:
            print("Hubo un error: ",str(e))

    @database_sync_to_async
    def cantidadJugadores(self,capitan):
        return capitan.equipos.jugadores.count()