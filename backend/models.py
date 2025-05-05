from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Server1(models.Model):
    nombre = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)
    avala = models.CharField(max_length=100)
    usuario_remoto = models.CharField(max_length=50)  # Nuevo campo
    timestamp = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre


class BackupConfig(models.Model):
    server_destino = models.ForeignKey(Server1, on_delete=models.CASCADE, related_name='respaldos_destino')
    server_remitente = models.ForeignKey(Server1, on_delete=models.CASCADE, related_name='respaldos_remitente')
    directorio_origen = models.CharField(max_length=255)
    directorio_destino = models.CharField(max_length=255)
    periodicidad = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, blank=True, null=True)