from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

class UsuarioForms(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["first_name","last_name","fecha_nacimiento","documento","num_document","celular","posicion","numero_camisa","foto","username","email"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type":"date"})
        }

    def clean(self):
        cleaned_date = super().clean()
        documento = cleaned_date.get('documento')
        numero_documento = cleaned_date.get("num_document").strip()
        if documento == "C.C":
            if not numero_documento.isdigit():
                raise forms.ValidationError("Casilla Número de documento; solo se aceptan numeros, porfavor no introducir letras")
            elif len(numero_documento) > 10:
                raise forms.ValidationError("Recuerda escribr el numero del documento valido")
        return cleaned_date
