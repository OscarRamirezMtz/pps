from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Server1(models.Model):
    nombre = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)
    avala = models.CharField(max_length=100)
    usuario_remoto = models.CharField(max_length=50)  # Nuevo campo
    timestamp = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class OTPCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    creado = models.DateTimeField(auto_now_add=True)

    def expirado(self):
        return timezone.now() > self.creado + timedelta(minutes=5)
    

class OTPIntento(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_attempt')
    intentos = models.IntegerField(default=0)
    bloqueado = models.DateTimeField(null=True, blank=True)

    def is_locked(self):
        return self.bloqueado and self.bloqueado > timezone.now()