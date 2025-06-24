from __future__ import annotations
from datetime import timedelta
from pathlib import Path
import paramiko, logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import ( authenticate, get_user_model, login as auth_login, logout as auth_logout )
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, ServidorForm, ServicioConfiguradoForm
from .models import OTPCode, OTPIntento, Servidor, ServicioConfigurado
from .utils import ( ejecutar_comando_remoto, generate_otp, mandar_mensaje )

logger = logging.getLogger("servidores_app")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Silenciar paramiko
logging.getLogger("paramiko").setLevel(logging.WARNING)

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
    """
    Cierre de sesión
    """
    auth_logout(request)
    return redirect("login")

@require_http_methods(["GET"])
@login_required(login_url='/login/')
def index(request):
    """
    Muestra la pagina principal a los usuarios logueados
    """     
    return render(request, 'index.html')

@require_http_methods(["GET", "POST"])
@login_required
def servidor_crear(request):
    """
    Maneja la Logica para agregar un servidor nuevo
    establece la conexion SSH al servidor
    copia la clave SSH
    si todo es correcto
    agrega el servidor a la BD
    """    
    if request.method == "POST":
        form = ServidorForm(request.POST)
        if form.is_valid():
            datos_servidor_dict = {
                'hostname': form.cleaned_data['direccion_host'],
                'username': form.cleaned_data['usuario_remoto'],
                'port': form.cleaned_data['ssh_port'],
            }
            password = form.cleaned_data['password']
            ssh_connection = None
            
            try:
                # Conexión SSH al servidor
                ssh_connection = paramiko.SSHClient()
                ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_connection.connect(**datos_servidor_dict, password=password, timeout=10)

                # Copiar clave SSH
                key_filepath = Path(settings.BASE_DIR) / '.ssh_keys' / 'app_id_rsa.pub'
                with open(key_filepath, 'r') as f:
                    public_key_string = f.read().strip()
                
                comando_ssh_key = f"mkdir -p ~/.ssh; chmod 700 ~/.ssh; touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys; grep -qF '{public_key_string}' ~/.ssh/authorized_keys || echo '{public_key_string}' >> ~/.ssh/authorized_keys"
                stdin, stdout, stderr = ssh_connection.exec_command(comando_ssh_key)
                if stdout.channel.recv_exit_status() != 0:
                    raise Exception(f"Falló al instalar la clave SSH: {stderr.read().decode()}")

                # Guardado en la BD
                servidor_instance = form.save(commit=False)
                servidor_instance.registrado_por = request.user
                servidor_instance.save()
                messages.success(request, f"Servidor '{servidor_instance.nombre}' registrado y configurado exitosamente")
                logger.info(f'Servidor registrado {datos_servidor_dict}')
                return redirect('servidor_listar')
                

            except Exception as e:
                form.add_error(None, f"Error no se pudo conectar al servidor: {e}")
            finally: # cierra la conexion SSH
                if ssh_connection:
                    ssh_connection.close()
    else:
        form = ServidorForm()
    
    context = {"form": form, "titulo": "Registrar y Configurar Servidor"}
    return render(request, "servidor_form.html", context)


def servidor_listar(request):
    """
    Muestra los servidores registrados
    """    
    servidores = Servidor.objects.filter(registrado_por=request.user)
    context = {"servidores": servidores, "titulo": "Mis Servidores Registrados"}
    return render(request, "servidor_listar.html", context) 

@login_required
def servidor_eliminar(request, pk):
    """
    Elimina el servidor de la BD
    """    
    servidor = get_object_or_404(Servidor, pk=pk, registrado_por=request.user)
    # Eliminamos el servidor de la base de datos
    nombre_servidor = servidor.nombre
    servidor.delete()
    messages.success(request, f"El servidor '{nombre_servidor}' ha sido eliminado de la plataforma.")
    logger.info(f'Servidor registrado {servidor.direccion_host}')
    return redirect('servidor_listar')

@login_required(login_url="login")
def servidor_detalle(request, servidor_pk):
    """
    Muestra detalles del servidor
    """    
    servidor = get_object_or_404(Servidor, pk=servidor_pk)
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
    """
    Maneja la logia para configurar un servicio nuevo
    """    
    servidor = get_object_or_404(Servidor, pk=servidor_pk, registrado_por=request.user)
    #solo el usuario que registro el servidor puede registrar servicios en este
    if hasattr(servidor, 'registrado_por') and servidor.registrado_por != request.user and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para configurar servicios en este servidor.")
        return redirect('servidor_detalle', servidor_pk=servidor_pk)

    if request.method == "POST":

        form = ServicioConfiguradoForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.servidor = servidor
            servicio.configurado_por = request.user
            try:
                servicio.save()
                messages.success(request, f"Servicio '{servicio.nombre_servicio_remoto}' configurado exitosamente para '{servidor.nombre}'.")
                logger.info(f'Servicio registrado {servicio.nombre_servicio_remoto} por {servidor.registrado_por}')
                return redirect('servidor_detalle', servidor_pk=servidor.pk)
            except Exception as e:
                messages.error(request, f"Error al guardar la configuración del servicio: {e}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:

        form = ServicioConfiguradoForm()

    context = {
        'form': form,
        'servidor': servidor,
        'titulo': f"Configurar Nuevo Servicio en {servidor.nombre}"
    }

    return render(request, 'servicio_configurar_form.html', context)

@login_required(login_url="login")
@require_http_methods(["POST"])
def servicio_accion(request, servicio_pk, accion):
    """
    Ejecuta las acciones iniciar, detener, reiniciar y verificar estado de los servidores
    """    
    servicio = get_object_or_404(ServicioConfigurado, pk=servicio_pk, servidor__registrado_por=request.user)
    servidor = servicio.servidor
    if hasattr(servidor, 'registrado_por') and servidor.registrado_por != request.user and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para ejecutar acciones en este servicio.")
        return redirect('servidor_detalle', servidor_pk=servidor.pk)
    comandos_map = {
        'levantar': f"systemctl start {servicio.nombre_servicio_remoto}",
        'bajar': f"systemctl stop {servicio.nombre_servicio_remoto}",
        'reiniciar': f"systemctl restart {servicio.nombre_servicio_remoto}",
        'verificar_estado': f"systemctl is-active {servicio.nombre_servicio_remoto}"
    }
    if accion not in comandos_map:
        messages.error(request, "Acción desconocida.")
        return redirect('servidor_detalle', servidor_pk=servidor.pk)
    comando_a_ejecutar = comandos_map[accion]
    resultado_ssh = ejecutar_comando_remoto(servidor, comando_a_ejecutar)
    servicio.ultima_comprobacion_estado = timezone.now()
    if resultado_ssh['error_conexion']:
        messages.error(request, f"Fallo de conexión al ejecutar '{accion}': {resultado_ssh['error_conexion']}")
        servicio.estado_conocido = 'error_verificacion'
    elif accion == 'verificar_estado':
        stdout = resultado_ssh['stdout'].strip()
        if stdout == "active":
            servicio.estado_conocido = 'activo'
            messages.success(request, f"El servicio '{servicio.nombre_servicio_remoto}' está ACTIVO.")
        elif stdout == "inactive":
            servicio.estado_conocido = 'inactivo'
            messages.success(request, f"El servicio '{servicio.nombre_servicio_remoto}' está INACTIVO.")
        elif stdout == "failed":
            servicio.estado_conocido = 'error_verificacion'
            messages.error(request, f"El servicio '{servicio.nombre_servicio_remoto}' tiene un estado FALLIDO.")
        else:
            servicio.estado_conocido = 'desconocido'
            messages.warning(request, f"Estado no reconocido: '{stdout}'.")
    else:
        if resultado_ssh['exit_code'] == 0:
            messages.success(request, f"Acción '{accion}' para '{servicio.nombre_servicio_remoto}' enviada con éxito.")
            
            if accion == 'levantar' or accion == 'reiniciar':
                servicio.estado_conocido = 'activo'
                messages.info(request, "Estado actualizado a 'Activo'.")
                logger.info(f'Servicio {servicio.nombre_servicio_remoto} se inicio por {servidor.registrado_por}')
            elif accion == 'bajar':
                servicio.estado_conocido = 'inactivo'
                messages.info(request, "Estado actualizado a 'Inactivo' (optimista).")
                logger.info(f'Servicio {servicio.nombre_servicio_remoto} se detuvo por {servidor.registrado_por}')
        else:
            messages.error(request, f"Falló la acción '{accion}' para '{servicio.nombre_servicio_remoto}'.")
            servicio.estado_conocido = 'error_verificacion'
            if resultado_ssh['stderr']:
                messages.warning(request, f"Error reportado: {resultado_ssh['stderr']}")
    servicio.save()
    return redirect('servidor_detalle', servidor_pk=servidor.pk)

@login_required(login_url="login")
def dashboard_view(request):
    """
    Muestra el dashboard de los servidores y servicios
    """
    servidores = Servidor.objects.filter(
        registrado_por=request.user
    ).prefetch_related('servicios_configurados')
    total_servidores = servidores.count()
    total_servicios = ServicioConfigurado.objects.filter(servidor__in=servidores).count()
    servicios_por_estado = ServicioConfigurado.objects.filter(
        servidor__in=servidores
    ).values('estado_conocido').annotate(cantidad=Count('estado_conocido'))
    context = {
        'servidores': servidores,
        'total_servidores': total_servidores,
        'total_servicios': total_servicios,
        'servicios_por_estado': list(servicios_por_estado),
        'titulo': "Dashboard de Monitoreo"
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url="login")
def api_dashboard_status(request):
    """
    verifica el estado de los servicios
    """
    servidores = Servidor.objects.filter(registrado_por=request.user)
    response_data = []
    for servidor in servidores:
        servidor_data = {
            'id': servidor.id,
            'nombre': servidor.nombre,
            'servicios': []
        }
        for servicio in servidor.servicios_configurados.all():
            comando = f"systemctl is-active {servicio.nombre_servicio_remoto}"
            resultado_ssh = ejecutar_comando_remoto(servidor, comando)
            estado_real_actual = servicio.estado_conocido
            if resultado_ssh['error_conexion']:
                estado_real_actual = 'error_verificacion'
            else:
                stdout = resultado_ssh['stdout'].strip()
                if stdout == "active":
                    estado_real_actual = 'activo'
                elif stdout == "inactive":
                    estado_real_actual = 'inactivo'
                elif stdout == "failed":
                    estado_real_actual = 'error_verificacion'
                else:
                    estado_real_actual = 'desconocido'
#se actualiza el estado del servicio en la bd
            if servicio.estado_conocido != estado_real_actual:
                servicio.estado_conocido = estado_real_actual
                servicio.save()
            
            servidor_data['servicios'].append({
                'id': servicio.id,
                'nombre': servicio.nombre_servicio_remoto,
                'estado': servicio.estado_conocido,
                'estado_display': servicio.get_estado_conocido_display(),
            })
            
        response_data.append(servidor_data)
        
    return JsonResponse({'servidores': response_data})