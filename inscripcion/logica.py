from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Torneo.services import equiposInscritos
from .services import foundInscription
import json

class ConfirmarInscripcion(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            data = json.loads(request.body)
            inscripcion_pk = data.get('inscripcion_pk',None)
            accion = data.get('accion',None)
            
            inscripcion = foundInscription(inscripcion_pk)
            
            if accion == 'aceptar':
                inscripcion.estado = 'aceptado'
                inscripcion.save()
                return JsonResponse({'exito':f'Equipo verificado y admitido al torneo'})
            elif accion == 'rechazar':
                inscripcion.estado = 'rechazado'
                inscripcion.save()
                return JsonResponse({'message':'Solicitud de inscripcion rechazada'})
            return JsonResponse({'error':'Acción no reconocida'},status=400)
        except Exception as e:
            return JsonResponse({'error':f'Ha pasado un error desde el servidor: {str(e)}'},status=500)
        
class TorneoEquipoInscrito(View):
    def get(self,request,*args,**kwargs):
        try:
            torneo_id = kwargs['torneo_id']
            if torneo_id:
                equipos = equiposInscritos(torneo_id)
                if equipos is not None:
                    return JsonResponse({'equipos':equipos},safe=True)
                return JsonResponse({'error':'No hay equipos inscritos en el momento'})
        except Exception as e:
            print('Error: ',str(e))