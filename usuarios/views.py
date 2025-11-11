from django.shortcuts import render
from django.views.generic import CreateView,TemplateView,DetailView
from django.contrib.auth.views import LoginView,LogoutView
from .models import Usuario
from .forms import UsuarioForms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SignUp(CreateView):
    model = Usuario
    form_class = UsuarioForms
    template_name = 'usuarios/signup.html'
    success_url = reverse_lazy('login')

class Login(LoginView):
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('Home:plataforma')

class Logout(LogoutView):
    next_page = reverse_lazy('login')

class MiPerfil(LoginRequiredMixin,DetailView):
    model = Usuario
    template_name = 'usuarios/miperfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return Usuario.objects.filter(pk=self.request.user.pk).first()
