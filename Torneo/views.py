from django.shortcuts import render
from django.views.generic import DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Torneo
from django.utils import timezone
from .services import obtener_estado_incripcion

# Create your views here.

hoy = timezone.now()

class Torneos(LoginRequiredMixin,ListView):
    model = Torneo
    queryset = Torneo.objects.all()
    template_name = 'torneo/torneos.html'
    context_object_name = 'torneos'

class TorneoEtapaInscripcion(LoginRequiredMixin,DetailView):
    model = Torneo
    template_name = 'torneo/torneo_inscripcion.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(obtener_estado_incripcion(self.request.user,self.get_object()))
        return context

class TorneoActivo(LoginRequiredMixin,DetailView):
    model = Torneo
    template_name = 'torneo/torneo_en_curso.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        torneo = self.get_object()
        context["grupos"] = torneo.grupo_set.all()
        context['fechas'] = torneo.partidos.all().values_list('jornada',flat=True).order_by('jornada').distinct()
        context['fechas2'] = torneo.partidos.filter(estado='finalizado').values_list('jornada',flat=True).order_by('jornada').distinct()
        return context
    
class TorneoEtapaProgramado(LoginRequiredMixin,DetailView):
    model = Torneo
    queryset = Torneo.objects.all()
    template_name = 'torneo/torneo_programado.html'
    context_object_name = 'torneo'