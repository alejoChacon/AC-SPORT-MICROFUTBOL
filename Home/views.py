from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.utils import timezone
from usuarios.models import Usuario
from Torneo.models import Torneo as Charala,Equipo
from django.http import JsonResponse
from .models import NotificacionSolicitud
import json
import random
# Create your views here.

#hoy = timezone.now()

def leerNotificacion(notificacionpk):
    try:
        if notificacionpk:
            n = NotificacionSolicitud.objects.get(pk=notificacionpk)
            n.leida = True
            n.accion = True
            n.save()
    except Exception as e:
        print('Ocurrio un error: ',str(e))

class PageStart(TemplateView):
    template_name = 'pagina_inicio.html'

class Plataforma(TemplateView):
    template_name = 'plataforma.html'

class Inicio(LoginRequiredMixin,TemplateView):
    template_name = 'home/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        torneos = Charala.objects.filter(inscripciones__equipo__jugadores=self.request.user)
        context["torneos"] = torneos 
        context["usuario"] = Usuario.objects.filter(pk=self.request.user.pk).first()
        context['notificaciones'] = NotificacionSolicitud.objects.filter(receptor=self.request.user,accion=False)
        return context

class RegistrarJugadorPorSolicitud(View):
    def post(self,request,*args,**kwargs):
        try:
            #pasamos los datos de Json a objeto de python
            data = json.loads(request.body)
            print(data)
            #Almacenamos los datos del objeto python en variables
            equipo_pk = data.get('equipo_pk')
            accion = data.get('accion')
            usuario_pk = data.get('usuario_pk')
            notificacion_pk = data.get('notificaion_pk')
            user = Usuario.objects.get(pk=usuario_pk)
            print(equipo_pk,accion,usuario_pk,notificacion_pk)
            if accion == 'aceptar':
                if user.equipos:
                    return JsonResponse({'error':f'Error, {user.get_full_name()} ya esta registrado en el equipo {user.equipos.nombre}'})
                equipo = Equipo.objects.get(pk=equipo_pk)
                if equipo.jugadores.count() >= 10:
                    print('Ha entrado')
                    leerNotificacion(notificacion_pk)
                    return JsonResponse({'error':f'Tardaste en aceptar la solicitud, !alguien ha tomado tú puesto!. ¿Por qué no hablas con el capitan del equipo? '})
                lista_numeros_de_camisa = equipo.jugadores.all().values_list('numero_camisa',flat=True)
                if user.numero_camisa in lista_numeros_de_camisa:
                    rango_completo = list(range(1,101))
                    numeros_de_camisa_sin_jugador = [n for n in rango_completo if n not in lista_numeros_de_camisa]
                    resultado = random.choice(numeros_de_camisa_sin_jugador)
                    user.numero_camisa = resultado
                    user.save()
                if user and equipo:
                    user.equipos = equipo
                    user.save()
                    notificacion = NotificacionSolicitud.objects.get(pk=notificacion_pk)
                    notificacion.accion = True
                    notificacion.leida = True
                    notificacion.save()
                    return JsonResponse({'message':f'¡{user.get_full_name()} exitos en tu nuevo equipo!'})
                
            elif accion == 'rechazar':
                notificacion = NotificacionSolicitud.objects.get(pk=notificacion_pk)
                notificacion.leida = True
                notificacion.accion = True
                notificacion.save()
                return JsonResponse({'message':f'Se ha negado la suscripcion del jugador {user.get_full_name()}'})
            
        except Usuario.DoesNotExist:
            return JsonResponse({"error":'Usuario No encontrado'})
        except Exception as e:
            return JsonResponse({'error':str(e)})