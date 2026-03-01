from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import IncidenciaPartido
from Torneo.models import Torneo
from partidos.models import Partido
from Torneo.services import jornadas_del_torneo
from partidos.services import partidos_de_hoy
from . import services
from miequipo.services import nomina_equipo_local,nomina_equipo_visitante

# Create your views here.

class VistaResultadosActas(LoginRequiredMixin,TemplateView):
    template_name = 'actas/general_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['torneos_activos'] = Torneo.objects.filter(estado='en_curso',representante = self.request.user)
        return context

class FechaTorneos(LoginRequiredMixin,DetailView):
    model = Torneo
    queryset = Torneo.objects.all()
    template_name = 'actas/fechas_torneo.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['jornadas'] = jornadas_del_torneo(self.get_object().pk)
        context['partidos_hoy'] = partidos_de_hoy(self.get_object().pk)
        return context
    
class VistaRegistrarMarcadores(LoginRequiredMixin,ListView):
    model = Partido
    template_name = 'actas/partidos_de_la_jornada.html'  
    context_object_name = 'partidos'

    def get_queryset(self):
        return Partido.objects.filter(torneo__pk=self.kwargs['torneo_pk'],jornada=self.kwargs['jornada']).exclude(estado='pendiente')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(services.obtener_datos_de_la_fecha(self.kwargs['torneo_pk'],self.kwargs['jornada']))
        return context

class PartidoEnVivo(LoginRequiredMixin,DetailView):
    model = Partido
    queryset = Partido.objects.all()
    template_name = 'actas/partido_en_vivo.html'
    context_object_name = 'partido'

class DetallesActa(LoginRequiredMixin,DetailView):
    model = Partido
    queryset = Partido.objects.all()
    template_name = 'actas/detalle_partido.html'
    context_object_name = 'partido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidenciasdelpartido'] = services.incidencias_del_partido(self.get_object().pk)
        return context
    
class GestionarActa(LoginRequiredMixin,DetailView):
    model = Partido
    queryset = Partido.objects.all()
    template_name = 'actas/ejemplo100.html'
    context_object_name = 'partido'