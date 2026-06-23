from django import forms
from django.core.exceptions import ValidationError
from .models import Alumno


class AlumnoCreateForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'DNI', 'MontoDeuda']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'required': True}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido', 'required': True}),
            'DNI': forms.NumberInput(attrs={'placeholder': 'DNI', 'required': True}),
            'MontoDeuda': forms.NumberInput(attrs={'placeholder': 'Monto de deuda', 'min': '0', 'step': '0.01'}),
        }

    def clean_DNI(self):
        dni = self.cleaned_data['DNI']
        if Alumno.objects.filter(DNI=dni).exists():
            raise ValidationError('Ya existe un alumno registrado con ese DNI.')
        return dni
