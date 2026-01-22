from django.views.generic import View
from Torneo.models import Equipo
from django.http import JsonResponse
from django.db.models import Q

class SearchTeam(View):
    def get(self,request,*args,**kwargs):
        equipos_menos_de_10_jugadores = Equipo.objects.filter(Q(jugadores__lt=10)|Q(jugadores__isnull=True)).values_list('id','nombre','capitan__first_name').distinct()
        equipos_menos_de_10_jugadores = list(equipos_menos_de_10_jugadores)
        return JsonResponse(equipos_menos_de_10_jugadores,safe=False)