from django.db import models
import uuid

# Create your models here.
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


class OTPCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    creado = models.DateTimeField(auto_now_add=True)

    def expirado(self):
        return timezone.now() > self.creado + timedelta(minutes=3)

class OTPIntento(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_attempts')
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    intentos = models.IntegerField(default=0)
    bloqueado = models.DateTimeField(null=True, blank=True)

    def is_locked(self):
        return self.bloqueado and self.bloqueado > timezone.now()

    class Meta:
        unique_together = ('user', 'direccion_ip')

class Servidor(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Servidor")
    direccion_host = models.GenericIPAddressField(unique=True, verbose_name="Dirección IP")
    usuario_remoto = models.CharField(max_length=50, verbose_name="Usuario Remoto SSH")
    ssh_port = models.PositiveIntegerField(default=22, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"
        ordering = ['nombre']

class ServicioConfigurado(models.Model):
    ESTADO_CHOICES = [
        ('desconocido', 'Desconocido'),
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('error_verificacion', 'Error al Verificar'),
    ]
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE, related_name="servicios_configurados")
    nombre_servicio_remoto = models.CharField(max_length=100, verbose_name="Nombre del Servicio en systemd")
    descripcion_personalizada = models.TextField(blank=True, verbose_name="Descripción Personalizada")
    estado_conocido = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='desconocido')
    ultima_comprobacion_estado = models.DateTimeField(null=True, blank=True)
    habilitado_para_gestion = models.BooleanField(default=True, verbose_name="¿Gestión Habilitada?", help_text="Si está marcado, se mostrarán los botones de levantar, bajar y reiniciar.")
    log_ultima_accion = models.TextField(blank=True, verbose_name="Log de la Última Acción")


    def __str__(self):
        return f"{self.nombre_servicio_remoto} en {self.servidor.nombre}"

    class Meta:
        verbose_name = "Servicio Configurado"
        verbose_name_plural = "Servicios Configurados"
        unique_together = ('servidor', 'nombre_servicio_remoto')