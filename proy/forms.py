# from backend.models import Server1
# from django import forms
# from django.contrib.auth.models import User
# import re
# from backend.models import Server1
# from crontab import CronTab
# from django.contrib.auth.forms import AuthenticationForm
# from captcha.fields import CaptchaField



# class LoginForm(forms.Form):
#     username = forms.CharField(label='Usuario', max_length=64)
#     password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
#     captcha = CaptchaField()



# class FormServ(forms.Form):
#     nombre = forms.CharField(label="Nombre del servidor", max_length=50)
#     ip = forms.CharField(label="IP o dominio del servidor", max_length=100)
#     avala = forms.CharField(label="Avala", widget=forms.HiddenInput(), required=False)
#     usuario_remoto = forms.CharField(label="Usuario remoto", max_length=50)
    

#     def set_usuario(self, usuario_actual):
#         self.fields['avala'].initial = usuario_actual.username

#     def clean_ip(self):
#         ip = self.cleaned_data['ip']
#         ip_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

#         if not ip_pattern.match(ip):
#             raise forms.ValidationError('La dirección IP no es válida. Por favor, introduce una dirección IP válida.')

#         return ip

# class FormSend(forms.Form):
#     server_destino = forms.ModelChoiceField(queryset=Server1.objects.all(), label='Servidor destino')
#     server_remitente = forms.ModelChoiceField(queryset=Server1.objects.all(), label='Servidor remitente')
#     directorio_origen = forms.CharField(label='Directorio de origen', max_length=255)
#     directorio_destino = forms.CharField(label='Directorio de destino', max_length=255)
#     periodicidad = forms.CharField(
#         label='Periodicidad (Crontab)',
#         max_length=50,
#         help_text='Ingresa la periodicidad en formato Crontab. Ejemplo: "0 0 * * *" para ejecutar diariamente a la medianoche.'
#     )

#     def clean_periodicidad(self):
#         periodicidad = self.cleaned_data['periodicidad']

#         Patrón regex para verificar la validez de la periodicidad
#         patron_valido = re.compile(r'^(\*|[0-9]+)( (\*|[0-9]+)){4}$')

#         if not patron_valido.match(periodicidad):
#             raise forms.ValidationError('La periodicidad no es válida. Utiliza 5 números separados por espacios o asteriscos.')

#         Validar que la periodicidad sea válida para crontab
#         try:
#             cron = CronTab(tab=periodicidad)
#         except ValueError:
#             raise forms.ValidationError('La periodicidad no es válida para crontab.')

#         return periodicidad

#     def clean(self):
#         cleaned_data = super().clean()
#         return cleaned_data
