from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Inscripcion
from django.contrib.auth.mixins import LoginRequiredMixin
from Torneo.models import Torneo,Equipo

# Create your views here.

class IncripcionEquipoATorneo(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        try:
            torneo_nombre = request.POST.get("torneo")
            equipo_nombre = request.POST.get("equipo")
            observacion = request.POST.get("observacion")
            pago_comprobante = request.FILES.get("pago_comprobante")
            documento_identidad = request.FILES.get("documento_identidad")
            if torneo_nombre and equipo_nombre and pago_comprobante and documento_identidad:
                print("Aqui entro al condicional")
                torneo = Torneo.objects.get(nombre=torneo_nombre)
                equipo = Equipo.objects.get(nombre=equipo_nombre)
                inscripcion_torneo = Inscripcion.objects.create(
                    torneo = torneo,
                    equipo = equipo,
                    #estado = 'aceptado',
                    pago_comprobante = pago_comprobante,
                    documento_identidad = documento_identidad
                )
                return JsonResponse({"message":f"Equipo {equipo_nombre} inscrito en el torneo {torneo_nombre} exitosamente!"})
            else:
                print("Aqui entró, pero esta mal")
                return JsonResponse({"error":"hubo un problema en la sincronizacion de datos enviados"})
        except Exception as e:
            return JsonResponse({"error":str(e)})