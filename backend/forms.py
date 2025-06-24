from django import forms
from django.contrib.auth.models import User
import re
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from .models import Servidor, ServicioConfigurado

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=64)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    captcha = CaptchaField()

class ServidorForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña del Usuario Remoto",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "••••••••"
        }),
        required=True,
        help_text="Se usará una sola vez para configurar el acceso por clave SSH y sudo.",
    )

    class Meta:
        model = Servidor
        fields = ["nombre", "direccion_host", "usuario_remoto", "ssh_port"]
        widgets = {
            "nombre":          forms.TextInput(attrs={"class": "form-control"}),
            "direccion_host":  forms.TextInput(attrs={"class": "form-control"}),
            "usuario_remoto":  forms.TextInput(attrs={"class": "form-control"}),
            "ssh_port":        forms.NumberInput(attrs={"class": "form-control"}),
        }

class ServicioConfiguradoForm(forms.ModelForm):
    class Meta:
        model = ServicioConfigurado
        fields = [
            'nombre_servicio_remoto',
            'descripcion_personalizada',
            'habilitado_para_gestion',
        ]
        widgets = {
            'nombre_servicio_remoto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: apache2, nginx'}),
            'descripcion_personalizada': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'habilitado_para_gestion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_servicio_remoto': "Nombre del Servicio en el Servidor Remoto",
            'descripcion_personalizada': "Descripción Personalizada (Opcional)",
            'habilitado_para_gestion': "¿Habilitar la gestión (botones de acción) para este servicio?",
        }
        help_texts = {
            'nombre_servicio_remoto': "El nombre exacto del servicio como es conocido por systemd o init en el servidor remoto.",
        }