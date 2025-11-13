from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Torneo as Charala
from fase_de_grupos.models import EquipoGrupo
from partidos.models import Partido
from django.utils import timezone
from GOLEADOR.models import Goleador
from usuarios.models import Usuario
from django.db.models import Count

# Create your views here.

hoy = timezone.now()

class Torneo(LoginRequiredMixin,TemplateView):
    template_name = 'torneo/torneo2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["torneos"] = Charala.objects.all()
        return context

class TorneoEtapaInscripcion(LoginRequiredMixin,DetailView):
    model = Charala
    template_name = 'torneo/detalletorneo.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        torneo = self.get_object()
        user_equipo = getattr(self.request.user, 'equipos', None)
        if user_equipo:
            esta_inscrito = torneo.inscripciones.filter(equipo=user_equipo).exists()
            context["esta_inscrito"] = esta_inscrito
        else:
            context["esta_inscrito"] = False
        return context
    
class TorneoActivo(LoginRequiredMixin,DetailView):
    model = Charala
    template_name = 'torneo/auxiliar.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grupos"] = self.get_object().grupo_set.all()
        return context