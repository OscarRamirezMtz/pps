from backend.models import Server1
from django import forms
from django.contrib.auth.models import User
import re
from backend.models import Server1
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from .models import Servidor, ServicioConfigurado

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=64)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    captcha = CaptchaField()

class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = [
            'nombre',
            'direccion_host',
            'usuario_remoto',
            'ssh_port',
            'clave_ssh_configurada',
            'detalles_adicionales'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_host': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_remoto': forms.TextInput(attrs={'class': 'form-control'}),
            'ssh_port': forms.NumberInput(attrs={'class': 'form-control'}),
            'clave_ssh_configurada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'detalles_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'nombre': "Nombre del Servidor",
            'direccion_host': "Dirección IP o Dominio del Servidor",
            'usuario_remoto': "Usuario Remoto SSH",
            'ssh_port': "Puerto SSH",
            'clave_ssh_configurada': "¿Clave SSH ya configurada para acceso automatizado?",
            'detalles_adicionales': "Detalles Adicionales (Opcional)"
        }
        help_texts = {
            'direccion_host': "Ej: 192.168.1.100 o servidor.ejemplo.com",
            'usuario_remoto': "Usuario con el que la plataforma se conectará vía SSH.",
            'ssh_port': "Por defecto es 22.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puedes añadir más personalizaciones aquí si es necesario
        # Por ejemplo, si quieres hacer algún campo no requerido que el modelo sí lo es
        # pero se llenará automáticamente en la vista.


class FormSend(forms.Form):
    server_destino = forms.ModelChoiceField(queryset=Server1.objects.all(), label='Servidor destino')
    server_remitente = forms.ModelChoiceField(queryset=Server1.objects.all(), label='Servidor remitente')
    directorio_origen = forms.CharField(label='Directorio de origen', max_length=255)
    directorio_destino = forms.CharField(label='Directorio de destino', max_length=255)
    periodicidad = forms.CharField(
        label='Periodicidad (Crontab)',
        max_length=50,
        help_text='Ingresa la periodicidad en formato Crontab. Ejemplo: "0 0 * * *" para ejecutar diariamente a la medianoche.'
    )

    def clean_periodicidad(self):
        periodicidad = self.cleaned_data['periodicidad']

        # Patrón regex para verificar la validez de la periodicidad
        patron_valido = re.compile(r'^(\*|[0-9]+)( (\*|[0-9]+)){4}$')

        if not patron_valido.match(periodicidad):
            raise forms.ValidationError('La periodicidad no es válida. Utiliza 5 números separados por espacios o asteriscos.')

        # Validar que la periodicidad sea válida para crontab
        try:
            cron = CronTab(tab=periodicidad)
        except ValueError:
            raise forms.ValidationError('La periodicidad no es válida para crontab.')

        return periodicidad

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    
class ServicioConfiguradoForm(forms.ModelForm):
    class Meta:
        model = ServicioConfigurado
        fields = [
            'nombre_servicio_remoto',
            'descripcion_personalizada',
            'puerto_monitorizar',
            'comando_verificar_estado',
            'comando_levantar',
            'comando_bajar',
            'comando_reiniciar',
            'habilitado_para_gestion',
        ]
        widgets = {
            'nombre_servicio_remoto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: apache2, nginx, sshd'}),
            'descripcion_personalizada': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej: Servidor web principal'}),
            'puerto_monitorizar': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 80, 443 (opcional)'}),
            'comando_verificar_estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional: systemctl status [servicio]'}),
            'comando_levantar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional: systemctl start [servicio]'}),
            'comando_bajar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional: systemctl stop [servicio]'}),
            'comando_reiniciar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional: systemctl restart [servicio]'}),
            'habilitado_para_gestion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_servicio_remoto': "Nombre del Servicio en el Servidor Remoto",
            'descripcion_personalizada': "Descripción Personalizada (Opcional)",
            'puerto_monitorizar': "Puerto a Monitorizar (Opcional)",
            'comando_verificar_estado': "Comando Personalizado: Verificar Estado",
            'comando_levantar': "Comando Personalizado: Levantar",
            'comando_bajar': "Comando Personalizado: Dar de Baja",
            'comando_reiniciar': "Comando Personalizado: Reiniciar",
            'habilitado_para_gestion': "¿Habilitar gestión (levantar, bajar, reiniciar) desde la plataforma?",
        }
        help_texts = {
            'nombre_servicio_remoto': "El nombre exacto del servicio como es conocido por systemd o init en el servidor remoto.",
            'comando_verificar_estado': "Si se deja vacío, se intentará 'systemctl status [nombre_servicio_remoto]'.",
        }