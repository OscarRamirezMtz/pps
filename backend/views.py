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
    Server1,
)
from backend.forms import LoginForm, FormServ, FormSend
from backend.utils import generate_otp, mandar_mensaje

MAX_OTP_INTENTOS     = 3
MINUTOS_BLOQUEADO = 1
User = get_user_model()


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Primera fase del login:
    1. Valida usuario y contraseña
    2. Si son correctos, genera OTP y redirige a verificación
    """
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = User.objects.filter(username=form.cleaned_data["username"]).first()
        if not user:
            messages.error(request, "Credenciales inválidas.")
            return redirect("login")

        intento, _ = OTPIntento.objects.get_or_create(user=user)

        if intento.bloqueado and timezone.now() < intento.bloqueado:
            minutos = math.ceil((intento.bloqueado - timezone.now()).total_seconds() / 60)
            messages.error(request, f"Usuario bloqueado. Intenta en {minutos} minuto(s).")
            return redirect("login")

        if authenticate(request, username=user.username, password=form.cleaned_data["password"]):
            # contraseña correcta, genera OTP y salta al paso 2
            request.session["preauth_user_id"] = user.id
            code = generate_otp()
            OTPCode.objects.create(user=user, code=code)
            mandar_mensaje(f"Tu código OTP es: `{code}`\nCaduca en 5 min.")
            return redirect("otp_verification")


        intento.intentos += 1
        if intento.intentos >= MAX_OTP_INTENTOS:
            intento.bloqueado = timezone.now() + timedelta(minutes=MINUTOS_BLOQUEADO)
            messages.error(request, f"Demasiados intentos. Usuario bloqueado por {MINUTOS_BLOQUEADO} min.")
        else:
            restantes = MAX_OTP_INTENTOS - intento.intentos
            messages.error(request, f"Contraseña incorrecta. Te quedan {restantes} intento(s).")
        intento.save()
        return redirect("login")

    return render(request, "login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def otp_verification_view(request):
    """
    Segunda fase del login: verifica el código OTP.
    """
    uid = request.session.get("preauth_user_id")
    if not uid:
        messages.error(request, "Sesión inválida. Vuelve a iniciar sesión.")
        return redirect("login")

    user = get_object_or_404(User, pk=uid)
    intento, _ = OTPIntento.objects.get_or_create(user=user)

    if intento.bloqueado and timezone.now() < intento.bloqueado:
        mins = math.ceil((intento.bloqueado - timezone.now()).total_seconds() / 60)
        messages.error(request, f"Usuario bloqueado. Intenta en {mins} minuto(s).")
        return redirect("login")

    if request.method == "POST":
        otp = request.POST.get("otp", "").strip()
        codigo = OTPCode.objects.filter(user=user).order_by("-creado").first()

        es_valido = codigo and not codigo.expirado() and codigo.code == otp
        if not es_valido:
            intento.intentos += 1
            if intento.intentos >= MAX_OTP_INTENTOS:
                intento.bloqueado = timezone.now() + timedelta(minutes=MINUTOS_BLOQUEADO)
                messages.error(request, f"Demasiados intentos. Usuario bloqueado por {MINUTOS_BLOQUEADO} min.")
            else:
                restantes = MAX_OTP_INTENTOS - intento.intentos
                messages.error(request, f"OTP incorrecto. Te quedan {restantes} intento(s).")
            intento.save()
            return redirect("login")

        # OTP correcto
        intento.delete()
        auth_login(request, user)
        request.session.pop("preauth_user_id", None)
        return redirect("index")

    return render(request, "otp_verification.html")


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


def _ssh_user_exists(ip: str, usuario: str) -> bool:
    """
    Comprueba que `usuario@ip` sea un login SSH válido
    (suponemos que la clave pública ya está cargada).
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=usuario, timeout=5)
        ssh.close()
        return True
    except (paramiko.AuthenticationException, paramiko.SSHException):
        return False


@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def add_server(request):
    success = None
    form = FormServ(request.POST or None)
    form.set_usuario(request.user)          # añade automáticamente avala

    if request.method == "POST" and form.is_valid():
        nombre  = form.cleaned_data["nombre"]
        ip      = form.cleaned_data["ip"]
        uremoto = form.cleaned_data["usuario_remoto"]

        if not _check_ping(ip):
            messages.error(request, "Servidor inaccesible (ping fallido).")
        elif not _ssh_user_exists(ip, uremoto):
            messages.error(request, f'El usuario remoto "{uremotо}" no existe o no tiene acceso SSH.')
        else:
            Server1.objects.create(
                nombre=nombre,
                ip=ip,
                avala=request.user,
                usuario_remoto=uremotо,
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