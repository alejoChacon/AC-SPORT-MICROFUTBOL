from .models import Inscripcion

def foundInscription(pk):
    try:
        inscripcion = Inscripcion.objects.get(pk=pk)
        return inscripcion
    except Exception as e:
        print('Se ha presentado un error: ',e)
