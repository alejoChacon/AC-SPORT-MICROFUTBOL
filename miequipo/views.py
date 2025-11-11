from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Torneo.models import Equipo

# Create your views here.

class MiEquipo(LoginRequiredMixin,TemplateView):
    template_name = "miequipo/miequipo.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            if self.request.user.equipo:
                equipo = Equipo.objects.filter(jugadores__pk = self.request.user.pk).first()
                context["equipo"] = equipo
                context["jugadores"] = equipo.jugadores.count()
            else:
                context["jugadores"] = 0
        except Equipo.DoesNotExist:
            context["jugadores"] = 0
        return context
