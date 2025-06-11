from __future__ import annotations
from django.shortcuts import get_object_or_404, redirect, render
import math
import shlex
import subprocess
from datetime import timedelta
import paramiko
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from backend.models import (
    OTPIntento,
    OTPCode,
    Servidor,
    ServicioConfigurado
)
from backend.forms import (
    LoginForm,  
    ServidorForm,
    ServicioConfiguradoForm
)
from backend.utils import (
    generate_otp, 
    mandar_mensaje, 
    ejecutar_comando_ssh
)

MAX_OTP_INTENTOS = 3
SEGUNDOS_BLOQUEO = 30
User = get_user_model()

def ip_cliente(request):
    """
    obtiene la direccion ip del cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def _manejar_intento_bloqueado(request, intento):
    """
    Maneja la lógica si la IP/usuario ya está bloqueado y el bloqueo no ha expirado.
    Retorna True si está bloqueado y se manejó, False en caso contrario.
    """
    if intento.bloqueado and timezone.now() < intento.bloqueado:
        intento.bloqueado = timezone.now() + timedelta(seconds=SEGUNDOS_BLOQUEO)
        intento.save()
        messages.error(request, f"Esta IP sigue bloqueada para este usuario. El tiempo de bloqueo se ha reiniciado a {SEGUNDOS_BLOQUEO} segundos debido a un nuevo intento.")
        if "preauth_user_id" in request.session:
            request.session.pop("preauth_user_id", None)
        return True
    return False

def _manejar_fallo_de_autenticacion_o_otp(request, intento, tipo_fallo="credenciales", username_ingresado=None):
    """
    Maneja la lógica de un fallo (ya sea de credenciales/contraseña o de OTP).
    Incrementa intentos y bloquea si es necesario, usando MAX_OTP_INTENTOS como límite global.
    """
    intento.intentos += 1
    
    mensaje_especifico_fallo = "Contraseña incorrecta"
    if tipo_fallo == "otp":
        mensaje_especifico_fallo = "OTP incorrecto"

    user_identifier_log = f" para el usuario '{username_ingresado}'" if username_ingresado else ""

    if intento.intentos >= MAX_OTP_INTENTOS:
        intento.bloqueado = timezone.now() + timedelta(seconds=SEGUNDOS_BLOQUEO)
        messages.error(request, f"Demasiados intentos fallidos ({mensaje_especifico_fallo}) desde esta IP{user_identifier_log}. IP bloqueada para este usuario por {SEGUNDOS_BLOQUEO} segundos.")
    else:
        restantes = MAX_OTP_INTENTOS - intento.intentos
        messages.error(request, f"{mensaje_especifico_fallo}{user_identifier_log}. Te quedan {restantes} intento(s) en total desde esta IP para este usuario.")
    
    intento.save()
    
    if tipo_fallo == "otp" or (intento.intentos >= MAX_OTP_INTENTOS):
        request.session.pop("preauth_user_id", None)

def _validar_otp(user_obj, otp_ingresado):
    """
    Valida el código OTP ingresado.
    """
    codigo_otp_guardado = OTPCode.objects.filter(user=user_obj).order_by("-creado").first()
    if not codigo_otp_guardado:
        return False

    if hasattr(codigo_otp_guardado, 'expirado') and callable(getattr(codigo_otp_guardado, 'expirado')):
        if codigo_otp_guardado.expirado():
            return False 
    return codigo_otp_guardado.codigo == otp_ingresado

@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Primera fase del login: Valida user y contraseña.
    Si son correctos, genera OTP y redirige a verificación.
    """
    form = LoginForm(request.POST or None)
    direccion_cliente = ip_cliente(request)

    if request.method == "POST" and form.is_valid():
        username_ingresado = form.cleaned_data["username"]
        password_ingresada = form.cleaned_data["password"]

        user_obj = User.objects.filter(username=username_ingresado).first()

        if not user_obj:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return redirect("login")

        intento, _ = OTPIntento.objects.get_or_create(
            user=user_obj,
            direccion_ip=direccion_cliente,
            defaults={'intentos': 0, 'bloqueado': None}
        )

        if intento.bloqueado and timezone.now() >= intento.bloqueado:
            intento.intentos = 0
            intento.bloqueado = None
            intento.save()

        if _manejar_intento_bloqueado(request, intento):
            return redirect("login")

        authenticated_user = authenticate(request, username=username_ingresado, password=password_ingresada)

        if authenticated_user:
            request.session["preauth_user_id"] = authenticated_user.id
            codigo_otp_generado = generate_otp() # De utils.py

            OTPCode.objects.filter(user=authenticated_user).delete()
            OTPCode.objects.create(user=authenticated_user, codigo=codigo_otp_generado)
            
            mandar_mensaje(f"Tu código OTP es: `{codigo_otp_generado}`\nCaduca en 1 min.") # De utils.py
            
            return redirect("otp_verification")
        else:
            _manejar_fallo_de_autenticacion_o_otp(request, intento, tipo_fallo="credenciales", username_ingresado=username_ingresado)
            return redirect("login")

    return render(request, "login.html", {"form": form})

@require_http_methods(["GET", "POST"])
def otp_verification_view(request):
    """
    Segunda fase del login: verifica el código OTP.
    """
    uid = request.session.get("preauth_user_id")
    if not uid:
        messages.error(request, "Sesión inválida o expirada. Vuelve a iniciar sesión.")
        return redirect("login")

    user_obj = get_object_or_404(User, pk=uid)
    direccion_cliente = ip_cliente(request)

    intento, _ = OTPIntento.objects.get_or_create(
        user=user_obj,
        direccion_ip=direccion_cliente,
        defaults={'intentos': 0, 'bloqueado': None}
    )

    if intento.bloqueado and timezone.now() >= intento.bloqueado:
        intento.intentos = 0
        intento.bloqueado = None
        intento.save()

    if _manejar_intento_bloqueado(request, intento):
        return redirect("login")

    if request.method == "POST":
        otp_ingresado = request.POST.get("otp", "").strip()

        if _validar_otp(user_obj, otp_ingresado):
            intento.delete()
            auth_login(request, user_obj)
            request.session.pop("preauth_user_id", None)
            OTPCode.objects.filter(user=user_obj).delete()
            messages.success(request, "¡Inicio de sesión exitoso!")
            return redirect("index")
        else:
            _manejar_fallo_de_autenticacion_o_otp(request, intento, tipo_fallo="otp", username_ingresado=user_obj.username)
            return redirect("login")

    return render(request, "otp_verification.html", {"user_obj": user_obj})

@login_required(login_url="login")
def logout_view(request):
    auth_logout(request)
    return redirect("login")


@login_required(login_url="login")
def index(request):
    return render(request, "index.html")

def _check_ping(ip: str) -> bool:
    try:
        subprocess.check_output(["ping", "-c", "1", ip])
        return True
    except subprocess.CalledProcessError:
        return False

def _ssh_user_exists(ip: str, user: str) -> bool:
    """
    Comprueba que `user@ip` sea un login SSH válido
    (suponemos que la clave pública ya está cargada).
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=user, timeout=5)
        ssh.close()
        return True
    except (paramiko.AuthenticationException, paramiko.SSHException):
        return False

@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def add_server(request):
    success = None
    form = FormServ(request.POST or None)
    form.set_user(request.user)          # añade automáticamente avala

    if request.method == "POST" and form.is_valid():
        nombre  = form.cleaned_data["nombre"]
        ip      = form.cleaned_data["ip"]
        uremoto = form.cleaned_data["user_remoto"]

        if not _check_ping(ip):
            messages.error(request, "Servidor inaccesible (ping fallido).")
        elif not _ssh_user_exists(ip, uremoto):
            messages.error(request, f'El user remoto "{uremotо}" no existe o no tiene acceso SSH.')
        else:
            Server1.objects.create(
                nombre=nombre,
                ip=ip,
                avala=request.user,
                user_remoto=uremotо,
                detalles="Alta exitosa",
            )
            success = "Servidor guardado con éxito."

    context = {"form": form, "success_message": success}
    return render(request, "alta.html", context)

@login_required(login_url="login")
def list_servers(request):
    return render(request, "logs.html", {"logs": Server1.objects.all()})

@require_http_methods(["GET"])
@login_required(login_url='/login/')
def index(request):
     return render(request, 'index.html')

def _check_ping(host_address: str) -> bool:
    try:
        # Para dominios, ping podría no ser la mejor prueba de "accesibilidad" para SSH,
        # pero puede ser un primer filtro.
        subprocess.check_output(["ping", "-c", "1", host_address])
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError: # Si ping no está instalado o en el PATH
        messages.warning(request, "Comando 'ping' no encontrado. Saltando verificación de ping.")
        return True # O False, dependiendo de cómo quieras manejar esto

def _ssh_user_exists(host_address: str, user: str, port: int = 22) -> bool:
    """
    Comprueba que `user@host_address:port` sea un login SSH válido
    (suponemos que la clave pública ya está cargada o se manejará la autenticación).
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Usar el puerto del formulario o el por defecto del modelo Servidor
        ssh.connect(host_address, port=port, username=user, timeout=5)
        ssh.close()
        return True
    except (paramiko.AuthenticationException, paramiko.SSHException, TimeoutError, paramiko.ssh_exception.NoValidConnectionsError) as e:
        return False

@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def servidor_crear(request): # Renombrada de add_server para claridad
    if request.method == "POST":
        form = ServidorForm(request.POST)
        if form.is_valid():
            # Antes de guardar, asignamos el usuario que registra
            servidor_instance = form.save(commit=False)
            servidor_instance.registrado_por = request.user
            
            # Validaciones adicionales antes de guardar definitivamente
            host = servidor_instance.direccion_host
            usuario_ssh = servidor_instance.usuario_remoto
            puerto_ssh = servidor_instance.ssh_port

            # Podrías hacer el ping aquí, pero _ssh_user_exists es más crítico
            # if not _check_ping(host):
            #     messages.error(request, f"Servidor en '{host}' inaccesible (ping fallido).")
            # el form.save() abajo disparará la creación, así que el mensaje de error debe prevenir esto
            if not servidor_instance.clave_ssh_configurada:
                 # Si la clave no está configurada, al menos verificamos que el usuario/puerto/host sea alcanzable
                 # y el usuario exista. La clave se configurará después.
                if not _ssh_user_exists(host, usuario_ssh, puerto_ssh):
                    messages.error(request, f"No se pudo conectar o el usuario '{usuario_ssh}' no existe/no tiene acceso SSH en '{host}:{puerto_ssh}'. Verifica los datos o configura la clave SSH manualmente y marca la casilla.")
                    # No guardamos si la conexión SSH falla y la clave no está marcada como configurada
                else:
                    servidor_instance.save()
                    messages.success(request, f"Servidor '{servidor_instance.nombre}' registrado con éxito. Recuerda configurar la clave SSH si aún no lo has hecho.")
                    return redirect('servidor_listar') # Redirigir a la lista de servidores
            else: # Si el usuario marcó que la clave ya está configurada
                servidor_instance.save()
                messages.success(request, f"Servidor '{servidor_instance.nombre}' registrado con éxito.")
                return redirect('servidor_listar') # Redirigir a la lista de servidores
    else:
        form = ServidorForm()

    context = {"form": form, "titulo": "Registrar Nuevo Servidor"}
    return render(request, "servidor_form.html", context) # Asumiendo un template

def servidor_listar(request): # Renombrada de list_servers
    servidores = Servidor.objects.filter(registrado_por=request.user) # O todos: Servidor.objects.all()
    context = {"servidores": servidores, "titulo": "Mis Servidores Registrados"}
    return render(request, "servidor_listar.html", context) # Asumiendo un template

def servidor_eliminar(request, pk):
    # Obtener el servidor o devolver un 404 si no existe
    # Asegurarse de que el servidor pertenezca al usuario actual o que sea un superusuario
    # por seguridad, para que un usuario no pueda eliminar servidores de otro.
    servidor = get_object_or_404(Servidor, pk=pk)

    # Opcional: Comprobación de permisos más granular
    # if servidor.registrado_por != request.user and not request.user.is_superuser:
    #     messages.error(request, "No tienes permiso para eliminar este servidor.")
    #     return redirect('servidor_listar') # O a alguna página de error

    try:
        nombre_servidor = servidor.nombre
        servidor.delete()
        messages.success(request, f"El servidor '{nombre_servidor}' ha sido eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al intentar eliminar el servidor: {e}")
    
    return redirect('servidor_listar') # Redirigir de vuelta a la lista de servidores

@login_required(login_url="login")
def servidor_detalle(request, servidor_pk):
    servidor = get_object_or_404(Servidor, pk=servidor_pk)
    # Opcional: Verificar permisos si el servidor no debe ser visible para todos los admins
    # if servidor.registrado_por != request.user and not request.user.is_superuser:
    #     messages.error(request, "No tienes permiso para ver este servidor.")
    #     return redirect('servidor_listar')
        
    servicios = ServicioConfigurado.objects.filter(servidor=servidor)
    context = {
        'servidor': servidor,
        'servicios': servicios,
        'titulo': f"Detalles de {servidor.nombre}"
    }
    return render(request, 'servidor_detalles.html', context)

@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def servicio_configurar_crear(request, servidor_pk):
    servidor = get_object_or_404(Servidor, pk=servidor_pk)
    # Opcional: Verificar permisos más estrictos si es necesario
    if hasattr(servidor, 'registrado_por') and servidor.registrado_por != request.user and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para configurar servicios en este servidor.")
        return redirect('servidor_detalle', servidor_pk=servidor_pk)

    if request.method == "POST":
        # CORRECCIÓN 1: Usar ServicioConfiguradoForm
        form = ServicioConfiguradoForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.servidor = servidor
            servicio.configurado_por = request.user
            try:
                servicio.save()
                messages.success(request, f"Servicio '{servicio.nombre_servicio_remoto}' configurado exitosamente para '{servidor.nombre}'.")
                # CORRECCIÓN 2: Nombre correcto de la URL de redirección
                return redirect('servidor_detalle', servidor_pk=servidor.pk)
            except Exception as e:
                messages.error(request, f"Error al guardar la configuración del servicio: {e}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        # CORRECCIÓN 3: Usar ServicioConfiguradoForm() para instanciar en GET
        form = ServicioConfiguradoForm()

    context = {
        'form': form,
        'servidor': servidor,
        'titulo': f"Configurar Nuevo Servicio en {servidor.nombre}"
    }
    # CORRECCIÓN 4: Ruta completa a la plantilla para claridad
    return render(request, 'servicio_configurar_form.html', context)

@login_required(login_url="login")
@require_http_methods(["POST"])
def servicio_accion(request, servicio_pk, accion):
    servicio = get_object_or_404(ServicioConfigurado, pk=servicio_pk)
    servidor = servicio.servidor

    if hasattr(servidor, 'registrado_por') and servidor.registrado_por != request.user and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para ejecutar acciones en este servicio.")
        return redirect('servidor_detalle', servidor_pk=servidor.pk)

    if not servicio.habilitado_para_gestion:
        messages.warning(request, f"La gestión para el servicio '{servicio.nombre_servicio_remoto}' está deshabilitada.")
        return redirect('servidor_detalle', servidor_pk=servidor.pk)
    
    comando_a_ejecutar = ""
    accion_exitosa = False 

    if accion == 'levantar':
        comando_a_ejecutar = servicio.comando_levantar or f"sudo systemctl start {servicio.nombre_servicio_remoto}"
        messages.info(request, f"Simulando 'levantar' servicio: {servicio.nombre_servicio_remoto}. Comando: {comando_a_ejecutar}")
        accion_exitosa = True 
        servicio.estado_conocido = 'activo' 
        
    elif accion == 'bajar':
        comando_a_ejecutar = servicio.comando_bajar or f"sudo systemctl stop {servicio.nombre_servicio_remoto}"
        messages.info(request, f"Simulando 'bajar' servicio: {servicio.nombre_servicio_remoto}. Comando: {comando_a_ejecutar}")
        accion_exitosa = True 
        servicio.estado_conocido = 'inactivo'

    elif accion == 'reiniciar':
        comando_a_ejecutar = servicio.comando_reiniciar or f"sudo systemctl restart {servicio.nombre_servicio_remoto}"
        messages.info(request, f"Simulando 'reiniciar' servicio: {servicio.nombre_servicio_remoto}. Comando: {comando_a_ejecutar}")
        accion_exitosa = True
        servicio.estado_conocido = 'activo'

    elif accion == 'verificar_estado':
        comando_a_ejecutar = servicio.comando_verificar_estado or f"sudo systemctl status {servicio.nombre_servicio_remoto}"
        messages.info(request, f"Simulando 'verificar estado' de: {servicio.nombre_servicio_remoto}. Comando: {comando_a_ejecutar}")
        accion_exitosa = True
        # Aquí deberías obtener el estado real y actualizar 'servicio.estado_conocido'
        # servicio.estado_conocido = 'desconocido' # Temporalmente
        # Lógica de ejemplo para actualizar (necesitarías la salida real del comando):
        # if "active (running)" in resultado_ssh.stdout:
        #     servicio.estado_conocido = 'activo'
        # elif "inactive (dead)" in resultado_ssh.stdout:
        #     servicio.estado_conocido = 'inactivo'
        # else:
        #     servicio.estado_conocido = 'error_verificacion'

    else:
        messages.error(request, "Acción desconocida.")
        return redirect('servidor_detalle', servidor_pk=servidor.pk)

    if accion_exitosa: # O basado en el resultado real de la ejecución del comando SSH
        # servicio.log_ultima_accion = resultado_ssh.stdout + "\n" + resultado_ssh.stderr # Log real
        servicio.ultima_comprobacion_estado = timezone.now()
        servicio.save()
        messages.success(request, f"Acción '{accion}' (simulada) para '{servicio.nombre_servicio_remoto}' procesada.")
    else:
        messages.error(request, f"Falló la acción '{accion}' (simulada) para '{servicio.nombre_servicio_remoto}'.")
        # servicio.log_ultima_accion = resultado_ssh.stdout + "\n" + resultado_ssh.stderr # Log real
        # servicio.save()


    return redirect('servidor_detalle', servidor_pk=servidor.pk)