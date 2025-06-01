from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator

class Server1(models.Model):
    nombre = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)
    avala = models.CharField(max_length=100)
    usuario_remoto = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class OTPCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    creado = models.DateTimeField(auto_now_add=True)

    def expirado(self):
        return timezone.now() > self.creado + timedelta(minutes=1)


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
    """
    Representa un servidor Linux que será administrado por la plataforma.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True, # Es buena idea que el nombre sea único para identificarlo fácilmente
        verbose_name="Nombre del Servidor",
        help_text="Un nombre descriptivo y único para el servidor."
    )
    direccion_host = models.CharField(
        max_length=255, # Para admitir IPs (IPv4, IPv6) y nombres de dominio completos
        verbose_name="Dirección IP o Dominio",
        help_text="La dirección IP (ej: 192.168.1.10) o el nombre de dominio completo (ej: servidor.midominio.com) del servidor."
    )
    usuario_remoto = models.CharField(
        max_length=50,
        verbose_name="Usuario Remoto SSH",
        help_text="El nombre de usuario para conectarse al servidor vía SSH (ej: admin, root, ubuntu)."
    )
    ssh_port = models.PositiveIntegerField(
        default=22,
        validators=[MinValueValidator(1), MaxValueValidator(65535)], # Rango válido para puertos
        verbose_name="Puerto SSH",
        help_text="El puerto en el que el servidor escucha conexiones SSH. Por defecto es 22."
    )
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Referencia al modelo User activo (mejor práctica)
        on_delete=models.SET_NULL, # Si el admin se borra, el servidor no se borra, pero este campo queda null.
                                   # Considera models.PROTECT si no quieres que se borre un admin con servidores.
        null=True,
        blank=True, # Puede ser opcional o asignado automáticamente por el sistema al admin logueado.
        related_name="servidores_registrados",
        verbose_name="Administrador que registró"
    )
    clave_ssh_configurada = models.BooleanField(
        default=False,
        verbose_name="¿Clave SSH configurada?",
        help_text="Marcar si la clave pública de esta plataforma ya ha sido añadida al 'authorized_keys' del usuario remoto en el servidor para acceso sin contraseña."
    )
    detalles_adicionales = models.TextField(
        blank=True,
        null=True,
        verbose_name="Detalles Adicionales",
        help_text="Cualquier nota, descripción o información relevante sobre el servidor (ej: OS, propósito, recordatorios de seguridad específicos)."
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    ultima_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servidor Linux"
        verbose_name_plural = "Servidores Linux"
        ordering = ['nombre'] # Ordenar por nombre por defecto en el admin y consultas


class ServicioConfigurado(models.Model):
    """
    Representa un servicio específico configurado para ser gestionado en un Servidor.
    El administrador define qué servicio es y cómo interactuar con él.
    """
    ESTADO_CHOICES = [
        ('desconocido', 'Desconocido'),
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('error_verificacion', 'Error al Verificar'),
        ('levantando', 'Levantando...'),
        ('bajando', 'Dando de baja...'),
        ('reiniciando', 'Reiniciando...'),
    ]

    servidor = models.ForeignKey(
        Servidor,
        on_delete=models.CASCADE, # Si se borra el servidor, se borran sus servicios configurados
        related_name="servicios_configurados",
        verbose_name="Servidor Asociado"
    )
    nombre_servicio_remoto = models.CharField(
        max_length=100,
        verbose_name="Nombre del Servicio en el Servidor",
        help_text="El nombre real del servicio en el sistema Linux (ej: 'apache2', 'nginx', 'mysql', 'sshd'). Este nombre se usará para los comandos si no se especifican comandos personalizados."
    )
    descripcion_personalizada = models.TextField(
        blank=True,
        verbose_name="Descripción Personalizada",
        help_text="Una descripción opcional para este servicio configurado (ej: 'Servidor web principal', 'Base de datos de usuarios')."
    )
    estado_conocido = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='desconocido',
        verbose_name="Último Estado Conocido",
        help_text="El último estado detectado del servicio en el servidor remoto. Se actualiza mediante monitorización."
    )
    puerto_monitorizar = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        verbose_name="Puerto a Monitorizar (Opcional)",
        help_text="Si el servicio escucha en un puerto específico, indícalo aquí para una posible verificación de estado basada en el puerto."
    )
    # Comandos personalizados: si están vacíos, la lógica de la aplicación podría intentar comandos estándar.
    comando_verificar_estado = models.TextField(
        blank=True,
        verbose_name="Comando Personalizado para Verificar Estado",
        help_text="Opcional. Comando específico para verificar el estado de este servicio en el servidor remoto. Si se deja vacío, se intentarán comandos estándar (ej: 'systemctl status nombre_servicio_remoto')."
    )
    comando_levantar = models.TextField(
        blank=True,
        verbose_name="Comando Personalizado para Levantar Servicio",
        help_text="Opcional. Comando específico para iniciar/levantar este servicio. Si se deja vacío, se intentarán comandos estándar."
    )
    comando_bajar = models.TextField(
        blank=True,
        verbose_name="Comando Personalizado para Dar de Baja Servicio",
        help_text="Opcional. Comando específico para detener/dar de baja este servicio. Si se deja vacío, se intentarán comandos estándar."
    )
    comando_reiniciar = models.TextField(
        blank=True,
        verbose_name="Comando Personalizado para Reiniciar Servicio",
        help_text="Opcional. Comando específico para reiniciar este servicio. Si se deja vacío, se intentarán comandos estándar."
    )
    habilitado_para_gestion = models.BooleanField(
        default=True,
        verbose_name="¿Habilitado para Gestión desde Plataforma?",
        help_text="Desmarcar si no se desea que este servicio sea gestionable (levantar, bajar, reiniciar) a través de la plataforma, solo monitorización."
    )
    ultima_comprobacion_estado = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Última Comprobación de Estado",
        help_text="Cuándo se verificó por última vez el estado de este servicio."
    )
    log_ultima_accion = models.TextField(
        blank=True,
        verbose_name="Log de la Última Acción",
        help_text="Resultado o log de la última acción ejecutada sobre este servicio (levantar, bajar, reiniciar, verificar estado)."
    )
    configurado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Podría ser el admin que lo configura
        related_name="servicios_que_configuro",
        verbose_name="Configurado por"
    )
    fecha_configuracion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Configuración"
    )
    ultima_actualizacion_config = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización de Configuración"
    )

    def __str__(self):
        return f"{self.nombre_servicio_remoto} en {self.servidor.nombre}"

    class Meta:
        verbose_name = "Servicio Configurado en Servidor"
        verbose_name_plural = "Servicios Configurados en Servidores"
        # Un servicio (por su nombre) debe ser único por servidor
        unique_together = ('servidor', 'nombre_servicio_remoto')
        ordering = ['servidor__nombre', 'nombre_servicio_remoto']