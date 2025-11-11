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

class TorneoDetalleView(LoginRequiredMixin,DetailView):
    model = Charala
    template_name = 'torneo/detalletorneo.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.equipos:
            resultado = self.get_object().inscripciones.filter(equipo=self.request.user.equipos)
            context["esta_inscrito"] = True if resultado.exists() else False
        context["esta_inscrito"] = False
        return context
    
class TorneoActivo(LoginRequiredMixin,DetailView):
    model = Charala
    template_name = 'torneo/auxiliar.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grupos"] = self.get_object().grupo_set.all()
        context["proximos"] = self.get_object().partidos.filter(fecha_hora__gte=hoy)
        context["recientes"] = self.get_object().partidos.filter(estado="finalizado")
        goleadores = Usuario.objects.filter(goles__partido__torneo=self.get_object(),
                    goles__es_autogol=False).annotate(goles_totales=Count('goles')).order_by("-goles_totales")
        context["goleadores"] = goleadores
        return context