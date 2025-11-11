from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

class UsuarioForms(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["first_name","last_name","fecha_nacimiento","documento","num_document","celular","foto","username","email"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type":"date"})
        }

    def clean(self):
        cleaned_date = super().clean()
        documento = cleaned_date.get('documento')
        numero_documento = cleaned_date.get("num_document")
        if documento == "C.C":
            if not numero_documento.isdigit():
                raise forms.ValidationError("Solo se aceptan numeros")
            elif len(numero_documento) > 10:
                raise forms.ValidationError("Recuerda escribr el numero del documento valido")
        return cleaned_date
