# from proy import settings
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .forms import LoginForm, FormServ
# from backend.models import Server1
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django import forms
# from django.http import JsonResponse
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from backend.models import BackupConfig
# from django.shortcuts import render 
# from .forms import FormSend
# from django.contrib import messages
# from crontab import CronTab
# import subprocess
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from backend.models import Server1, BackupConfig
# import subprocess
# from django.shortcuts import render, redirect
# from .forms import FormSend
# from crontab import CronTab
# import re
# import subprocess
# from django.shortcuts import render
# from django.contrib import messages
# from .forms import FormServ
# import paramiko
# import shlex
# from django.db.models import Max
# from django.db.models import F
# from django.db import models
# from django.db.models import Max, CharField, IntegerField, Value
# from django.db.models.functions import Cast
# from django.db.models import Max
# from crontab import CronTab
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from crontab import CronTab
# from django.views.decorators.http import require_http_methods
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import login
# from backend.models import OTPCode
# from .utils import generate_otp, mandar_mensaje
# from .forms import LoginForm
# from datetime import timedelta
# import math, shlex, subprocess, paramiko
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout, get_user_model
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone
# from django.views.decorators.http import require_http_methods
# from backend.models import (
#     Server1,
#     BackupConfig,
#     OTPCode,
#     OTPAttempt,
# )
# from .forms import LoginForm, FormServ, FormSend
# from .utils import generate_otp, mandar_mensaje
# from django.utils import timezone
# from datetime import timedelta
# from backend.models import OTPCode, OTPAttempt


# MAX_OTP_ATTEMPTS = 3
# LOCKOUT_TIME_MINUTES = 1
# User = get_user_model()

# @require_http_methods(["GET", "POST"])
# def login_view(request):
#     form = LoginForm(request.POST or None)

#     if request.method == "POST" and form.is_valid():
#         username = form.cleaned_data["username"]
#         password = form.cleaned_data["password"]

#         user = User.objects.filter(username=username).first()
#         if not user:
#             messages.error(request, "Credenciales inválidas.")
#             return redirect("login")

#         intento, _ = OTPAttempt.objects.get_or_create(user=user)

#         # ¿está bloqueado?
#         if intento.locked_until and timezone.now() < intento.locked_until:
#             m = math.ceil((intento.locked_until - timezone.now()).total_seconds() / 60)
#             messages.error(request, f"Usuario bloqueado. Intenta en {m} minuto(s).")
#             return redirect("login")

#         # verificar contraseña
#         if authenticate(request, username=username, password=password):
#             #intento.delete()           # ← sólo existe si había intentos
#             request.session["preauth_user_id"] = user.id
#             code = generate_otp()
#             OTPCode.objects.create(user=user, code=code)
#             mandar_mensaje(f"Tu código OTP es: `{code}`\nCaduca en 5 min.")
#             return redirect("otp_verification")
#         else:
#             intento.attempts += 1
#             if intento.attempts >= MAX_OTP_ATTEMPTS:
#                 intento.locked_until = timezone.now() + timedelta(minutes=LOCKOUT_TIME_MINUTES)
#                 messages.error(
#                     request,
#                     f"Demasiados intentos. Usuario bloqueado por {LOCKOUT_TIME_MINUTES} minuto(s).",
#                 )
#             else:
#                 restantes = MAX_OTP_ATTEMPTS - intento.attempts
#                 messages.error(request, f"Contraseña incorrecta. Te quedan {restantes} intento(s).")
#             intento.save()
#             return redirect("login")

#     return render(request, "login.html", {"form": form})


# @require_http_methods(["GET"])
# @login_required(login_url='/login/')
# def index(request):
#     return render(request, 'index.html')


# #view para borrar la cookie de sesion y salirse de la pagina rediriendose al login
# from django.contrib.auth import logout
# def logout_v(request):
#     logout(request)
#     return redirect('/login/')

# #realiza un ping al equipo que queremos dar de alta
# def check_ping(ip):
#     try:
#         #ssubprocees funciona con tokens
#         #sen esta parte se utilzia checkoutput para verificar la salida del comando, ping, un paque icmp, una vez 
#         #a esa ip
#         subprocess.check_output(["ping", "-c", "1", ip])
#         return True  # Ping exitoso
#     except subprocess.CalledProcessError:
#         return False  # Ping fallido

# #DAR DE ALTA SERVIDORES EN EL SISTEMA WEB
# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/login/')
# def dar_alta(request):
#     #evita que se muestre un mnesaje de exito al cargar la vista
#     success_message = None
#     if request.method == 'POST':
#         #esto carga en una variable el usuario que esta logueado
#         usuario_actual = request.user
#         #crea una isntancia en la cual se guarda los datos enviados en formlario por post
#         form = FormServ(request.POST)
#         #mandas a la funcion del formulario apra agregar a avala el nombre del usuario actual
#         form.set_usuario(usuario_actual)

#         if form.is_valid():
#             #se asignan los valores del formulario a las variables
#             nombre = form.cleaned_data['nombre']
#             ip = form.cleaned_data['ip']

#             # Verificación de ping antes de guardar
#             #mandas a llamar la funcion, mandando como parametro la varibale ip
#             if check_ping(ip):
#                 #gaurdas en la variable el valor del usuario remoto eque esta en el formulario
#                 usuario_remoto = form.cleaned_data.get('usuario_remoto')

#                 # Verificación de existencia del usuario remoto mediante conexión SSH
#                 if check_user_existence(ip, usuario_remoto):
#                     try:
#                         server = Server1(
#                             nombre=nombre,
#                             ip=ip,
#                             avala=usuario_actual,
#                             usuario_remoto=usuario_remoto,
#                             detalles='Alta exitosa',
#                         )
#                         server.save()
#                         success_message = 'El servidor se ha guardado con éxito.'
#                     except Exception as e:
#                         messages.error(request, f'Ha ocurrido un error al guardar el servidor: {e}')
# #lo guarda para fines de mostras los logs de las altas
#                         server = Server1(
#                             nombre=nombre,
#                             ip=ip,
#                             avala=usuario_actual,
#                             usuario_remoto=usuario_remoto,
#                             detalles=f'Error al crear servidor: {e}',
#                         )
#                         server.save()
#                 else:
#                     messages.error(request, f'El usuario remoto "{usuario_remoto}" no existe en la dirección IP proporcionada.')
#             else:
#                 messages.error(request, 'No se puede conectar a la dirección IP proporcionada. Verifica la conexión y vuelve a intentarlo.')

#         else:
#             messages.error(request, 'El formulario no es válido. Por favor, revisa los datos introducidos.')

#     else:
#         form = FormServ()

#     return render(request, 'alta.html', {'form': form, 'success_message': success_message})
# #la view de arriba hace uso de esta funcion que lo que hace principalmente es verificar la existencia de 
# #un usuario en el servidor al cualquier queremos dar de alta, debemos tener compartidas las claves ssh 
# def check_user_existence(ip, usuario_remoto):
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(ip, username=usuario_remoto)
#         ssh.close()
#         return True
#     except paramiko.AuthenticationException:
#         return False
#     except paramiko.SSHException:
#         return False
#     except Exception as e:
#         return False

# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/login/')
# def ver_logs(request):
#     logs = Server1.objects.all()  
#     return render(request, 'logs.html', {'logs': logs})

# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# #from .models import OTPCode
# from backend.models import OTPCode
# from .utils import generate_otp, mandar_mensaje  # asegúrate de importar mandar_mensaje

# def request_otp(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         user = User.objects.filter(username=username).first()
#         if not user:
#             messages.error(request, "Usuario no encontrado")
#             return redirect("request_otp")

#         code = generate_otp()
#         OTPCode.objects.create(user=user, code=code)

#         mensaje = f"Código OTP para {user.username}: `{code}`\nCaduca en 5 minutos."
#         if mandar_mensaje(mensaje):
#             messages.success(request, "OTP enviado por Telegram")
#         else:
#             messages.error(request, "Error al enviar OTP por Telegram")

#         return redirect("verify_otp")
#     return render(request, "request_otp.html")

# @require_http_methods(["GET", "POST"])
# def otp_verification_view(request):
#     user_id = request.session.get("preauth_user_id")
#     if not user_id:
#         messages.error(request, "Sesión inválida. Vuelve a iniciar sesión.")
#         return redirect("login")

#     user      = get_object_or_404(User, pk=user_id)
#     intento, _ = OTPAttempt.objects.get_or_create(user=user)

#     # bloqueo activo
#     if intento.locked_until and timezone.now() < intento.locked_until:
#         mins = math.ceil((intento.locked_until - timezone.now()).total_seconds() / 60)
#         messages.error(request, f"Usuario bloqueado. Intenta en {mins} minuto(s).")
#         return redirect("login")

#     if request.method == "POST":
#         otp_ingresado = request.POST.get("otp", "").strip()
#         codigo = OTPCode.objects.filter(user=user).order_by("-created_at").first()

#         es_valido = (
#             codigo and
#             not codigo.is_expired() and
#             codigo.code == otp_ingresado
#         )

#         if not es_valido:
#             # ➜ sumar intento y decidir
#             intento.attempts += 1
#             if intento.attempts >= MAX_OTP_ATTEMPTS:
#                 intento.locked_until = timezone.now() + timedelta(minutes=LOCKOUT_TIME_MINUTES)
#                 intento.save()
#                 messages.error(
#                     request,
#                     f"Demasiados intentos. Usuario bloqueado por {LOCKOUT_TIME_MINUTES} minuto(s)."
#                 )
#             else:
#                 intento.save()
#                 restantes = MAX_OTP_ATTEMPTS - intento.attempts
#                 messages.error(request, f"OTP incorrecto. Te quedan {restantes} intento(s).")

#             return redirect("login")      # ← siempre volvemos al login

#         # OTP correcto ⇒ éxito total
#         intento.delete()                  # ahora sí, limpiamos el contador
#         login(request, user)
#         request.session.pop("preauth_user_id", None)
#         return redirect('/index/')

#     return render(request, "otp_verification.html")