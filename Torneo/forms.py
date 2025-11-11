from django import forms
from .models import Equipo

class EquipoForms(forms.ModelForm):
    class Meta:
        exclude = ["fecha_creacion","fecha_update","activo"]