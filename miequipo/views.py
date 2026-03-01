from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Torneo.models import Equipo
from usuarios.models import Usuario
from Torneo.forms import EquipoForms
from django.views import View
from fase_de_grupos.models import EquipoGrupo
from django.http import JsonResponse
from partidos.models import Partido
from Home.models import NotificacionSolicitud
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse_lazy

# Create your views here.

fecha_actual = timezone.now()

class MiEquipo(LoginRequiredMixin,TemplateView):
    template_name = "miequipo/miequipo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.user.equipos:
                equipo = Equipo.objects.filter(jugadores__pk = self.request.user.pk).first()
                alineacion = getattr(equipo,'titular_equipo',None)
                titulares_ids = []
                if alineacion:
                    titulares_ids = [
                        alineacion.portero.id, alineacion.cierre.id, alineacion.ala_izq_id,
                        alineacion.ala_der_id, alineacion.pivot.id
                    ]
                context['alineacion'] = alineacion
                context['titulares_ids'] = titulares_ids
                context["equipo"] = equipo
                context["jugadores"] = equipo.jugadores.count()
            else:
                print("Está entrando aquí")
                notificacion_del_dia = NotificacionSolicitud.objects.filter(remitente=self.request.user,fecha_creacion__day=fecha_actual.day)
                print(notificacion_del_dia)
                if len(notificacion_del_dia) >= 2:
                    context['cantidad_solicitud_dia_rta'] = False
                else:
                    context["cantidad_solicitud_dia_rta"] = True
            return context
        except Equipo.DoesNotExist:
            context["jugadores"] = 0
    
class MiEquipoInfo(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            equipo = EquipoGrupo.objects.get(equipo__pk=self.kwargs["equipo_pk"])
            equipo_info = {
                "partidos_jugados": equipo.partidos_jugados,
                "partidos_ganados": equipo.partidos_ganados,
                "partidos_empatados": equipo.partidos_empatados,
                "partidos_perdidos": equipo.partidos_perdidos
            }
            return JsonResponse({"equipo_info":equipo_info})
        except Exception as e:
            return JsonResponse({"error":str(e)})
        
from django.utils import timezone

class CalendarioPartidos(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            equipo = Equipo.objects.get(pk=self.kwargs["equipo_pk"])
            if self.kwargs["jornada"]:
                estado = self.kwargs["jornada"]
                calendario_partidos = Partido.objects.filter(Q(equipo_local=equipo) | Q(equipo_visitante=equipo),
                                    estado=estado,torneo=equipo.inscripciones_torneo.first().torneo).order_by('jornada')                
            else:
                calendario_partidos = Partido.objects.filter(Q(equipo_local=equipo) | Q(equipo_visitante=equipo),
                                    estado="programado",torneo=equipo.inscripciones_torneo.first().torneo).order_by('jornada')
            data_calendar = []
            for partido in calendario_partidos:
                local_hora = timezone.localtime(partido.fecha_hora)
                data_calendar.append({
                    "fecha": partido.fecha_hora.strftime("%d/%m/%Y"),
                    "rival": partido.equipo_local.nombre if partido.equipo_visitante.nombre == equipo.nombre else partido.equipo_visitante.nombre,
                    "resultado": partido.get_estado_display() if partido.estado in ["programado","en_juego"] else f"{partido.goles_local} : {partido.goles_visitante}",
                    "cancha": partido.cancha,
                    "hora": local_hora.strftime("%H:%M")
                })
            return JsonResponse({"calendario_partidos":data_calendar})
        except Exception as e:
            return JsonResponse({"error":str(e)})

class ActualizarEquipo(LoginRequiredMixin,UpdateView):
    model = Equipo
    template_name = 'miequipo/actualizarEquipo.html'
    queryset = Equipo.objects.all()
    form_class = EquipoForms
    success_url = reverse_lazy('miequipo:miequipo')

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['capitan'].queryset = Usuario.objects.filter(equipos=self.get_object())
        return form
