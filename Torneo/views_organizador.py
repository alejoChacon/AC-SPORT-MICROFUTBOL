from django.views.generic import TemplateView,DetailView
from .models import Torneo
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import cantidad_solicitudes_pendientes

class MisTorneos(LoginRequiredMixin,TemplateView):
    template_name = 'torneo/organizador/misfavoritos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['torneos'] = Torneo.objects.filter(representante=self.request.user.get_full_name())
        return context
    
class ValidacionINscripcion(LoginRequiredMixin,DetailView):
    model = Torneo
    queryset = Torneo.objects.all()
    template_name = 'torneo/organizador/inscripcion.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(cantidad_solicitudes_pendientes(self.get_object()))
        return context