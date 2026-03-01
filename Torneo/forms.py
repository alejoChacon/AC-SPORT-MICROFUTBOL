from django import forms
from .models import Equipo

class EquipoForms(forms.ModelForm):
    class Meta:
        model = Equipo
        exclude = ["fecha_creacion","fecha_update","activo"]
        widgets = {
            'nombre':forms.TextInput(attrs={'placeholder':'Ejem: Los Galacticos'}),
            'escudo':forms.FileInput(attrs={'class': 'input-file-custom'})
        }