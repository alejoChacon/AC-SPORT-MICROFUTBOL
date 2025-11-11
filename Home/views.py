from django.shortcuts import render
from django.views.generic import TemplateView
from usuarios.models import Usuario
from Torneo.models import Torneo as Charala

# Create your views here.

class PageStart(TemplateView):
    template_name = 'pagina_inicio.html'

class Plataforma(TemplateView):
    template_name = 'plataforma.html'

class Inicio(TemplateView):
    template_name = 'home/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        torneos = Charala.objects.filter(inscripciones__equipo__jugadores=self.request.user)
        context["torneos"] = torneos 
        context["usuario"] = Usuario.objects.filter(pk=self.request.user.pk).first()
        return context

