from proy import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, FormServ
from backend.models import Server1
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from backend.models import BackupConfig
from django.shortcuts import render 
from .forms import FormSend
from django.contrib import messages
from crontab import CronTab
import subprocess
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from backend.models import Server1, BackupConfig
import subprocess
from django.shortcuts import render, redirect
from .forms import FormSend
from crontab import CronTab
import re
import subprocess
from django.shortcuts import render
from django.contrib import messages
from .forms import FormServ
import paramiko
import shlex
from django.db.models import Max
from django.db.models import F
from django.db import models
from django.db.models import Max, CharField, IntegerField, Value
from django.db.models.functions import Cast
from django.db.models import Max
from crontab import CronTab
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from crontab import CronTab
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/index/')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@require_http_methods(["GET"])
@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


#view para borrar la cookie de sesion y salirse de la pagina rediriendose al login
from django.contrib.auth import logout
def logout_v(request):
    logout(request)
    return redirect('/login/')

#realiza un ping al equipo que queremos dar de alta
def check_ping(ip):
    try:
        #ssubprocees funciona con tokens
        #sen esta parte se utilzia checkoutput para verificar la salida del comando, ping, un paque icmp, una vez 
        #a esa ip
        subprocess.check_output(["ping", "-c", "1", ip])
        return True  # Ping exitoso
    except subprocess.CalledProcessError:
        return False  # Ping fallido

#DAR DE ALTA SERVIDORES EN EL SISTEMA WEB
@require_http_methods(["GET", "POST"])
@login_required(login_url='/login/')
def dar_alta(request):
    #evita que se muestre un mnesaje de exito al cargar la vista
    success_message = None
    if request.method == 'POST':
        #esto carga en una variable el usuario que esta logueado
        usuario_actual = request.user
        #crea una isntancia en la cual se guarda los datos enviados en formlario por post
        form = FormServ(request.POST)
        #mandas a la funcion del formulario apra agregar a avala el nombre del usuario actual
        form.set_usuario(usuario_actual)

        if form.is_valid():
            #se asignan los valores del formulario a las variables
            nombre = form.cleaned_data['nombre']
            ip = form.cleaned_data['ip']

            # Verificación de ping antes de guardar
            #mandas a llamar la funcion, mandando como parametro la varibale ip
            if check_ping(ip):
                #gaurdas en la variable el valor del usuario remoto eque esta en el formulario
                usuario_remoto = form.cleaned_data.get('usuario_remoto')

                # Verificación de existencia del usuario remoto mediante conexión SSH
                if check_user_existence(ip, usuario_remoto):
                    try:
                        server = Server1(
                            nombre=nombre,
                            ip=ip,
                            avala=usuario_actual,
                            usuario_remoto=usuario_remoto,
                            detalles='Alta exitosa',
                        )
                        server.save()
                        success_message = 'El servidor se ha guardado con éxito.'
                    except Exception as e:
                        messages.error(request, f'Ha ocurrido un error al guardar el servidor: {e}')
#lo guarda para fines de mostras los logs de las altas
                        server = Server1(
                            nombre=nombre,
                            ip=ip,
                            avala=usuario_actual,
                            usuario_remoto=usuario_remoto,
                            detalles=f'Error al crear servidor: {e}',
                        )
                        server.save()
                else:
                    messages.error(request, f'El usuario remoto "{usuario_remoto}" no existe en la dirección IP proporcionada.')
            else:
                messages.error(request, 'No se puede conectar a la dirección IP proporcionada. Verifica la conexión y vuelve a intentarlo.')

        else:
            messages.error(request, 'El formulario no es válido. Por favor, revisa los datos introducidos.')

    else:
        form = FormServ()

    return render(request, 'alta.html', {'form': form, 'success_message': success_message})
#la view de arriba hace uso de esta funcion que lo que hace principalmente es verificar la existencia de 
#un usuario en el servidor al cualquier queremos dar de alta, debemos tener compartidas las claves ssh 
def check_user_existence(ip, usuario_remoto):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=usuario_remoto)
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except paramiko.SSHException:
        return False
    except Exception as e:
        return False


#esta funcion se utiliza principalmente para actualizar la lista de servidores activos una vez
#se acceda a la pagina de respaldos de manera automatica
#def get_server_choices(request):
 #   servers = Server1.objects.all()
 #   choices = [{'id': server.id, 'nombre': server.nombre} for server in servers]
 #   return JsonResponse(choices, safe=False)




@require_http_methods(["GET", "POST"])
@login_required(login_url='/login/')
def ver_logs(request):
    logs = Server1.objects.all()  
    return render(request, 'logs.html', {'logs': logs})




#CREACION DE RESPALDOS EN EL CRONTAB
@require_http_methods(["GET", "POST"])
@login_required(login_url='/login/')
def crear_respaldo(request):
    if request.method == 'POST':
        form = FormSend(request.POST)
        if form.is_valid():
            # Obtener datos del formulario
            server_destino = form.cleaned_data['server_destino']
            server_remitente = form.cleaned_data['server_remitente']
            directorio_origen = form.cleaned_data['directorio_origen']
            directorio_destino = form.cleaned_data['directorio_destino']
            periodicidad = form.cleaned_data['periodicidad']
            # Verificar si los directorios existen en ambas máquinas
            if directorios_existen(server_remitente.usuario_remoto, server_remitente.ip, server_destino.usuario_remoto, server_destino.ip, directorio_origen, directorio_destino):
                # Configurar el cronjob con comentario
                cron = CronTab(user='hyper-lethal')
                job = cron.new(
                    #creas el comando con fstrings 
                    command=f'ssh {server_remitente.usuario_remoto}@{server_remitente.ip} "tar -czf - -C {directorio_origen} . | ssh {server_destino.usuario_remoto}@{server_destino.ip} \'cat > {directorio_destino}/backup_$(date +%Y-%m-%d_%H-%M-%S).tar.gz\'"',
                    #con el coment creado nosotros eliminamoss los cronjobs
                    comment=f'Respaldo de {server_remitente} a {server_destino} cada {periodicidad}'
                )
                #esto agrega la periodicidad al corntab
                job.setall(periodicidad)

                # Obtener el comentario y asignarlo al campo nuevo para agregarlo a la base de datos
                comentario = job.comment

                # Crear una instancia del modelo BackupConfig
                configuracion_respaldo = BackupConfig(
                    server_destino=server_destino,
                    server_remitente=server_remitente,
                    directorio_origen=directorio_origen,
                    directorio_destino=directorio_destino,
                    periodicidad=periodicidad,
                    comment=comentario,
                )
                configuracion_respaldo.save()

                #das de alta el cronjob
                cron.write()

                messages.success(request, 'Configuración de respaldo guardada correctamente.')
            else:
                messages.error(request, 'Uno o ambos directorios no existen en una o ambas máquinas remotas.')
        else:
            messages.error(request, 'Error al procesar el formulario. Por favor, verifica los datos ingresados.')
    else:
        form = FormSend()

    return render(request, 'niu.html', {'form': form})


def directorios_existen(usuario_remoto_remitente, ip_remota_remitente, usuario_remoto_destino, ip_remota_destino, directorio_origen, directorio_destino):
    try:
        # Verificar si los directorios existen en la máquina remitente
        #se usan fstrings para concatenar las variables a un texto plano que sera el comando
        #test -d es un coamndo que verifica que el directorio exista
        comando_remitente = f'ssh {usuario_remoto_remitente}@{ip_remota_remitente} test -d {directorio_origen} '
        #tokeisa con shlex, y se utiliza una misma salida /estatndar y error) mediante una sola para mayor 
        #facilidad
        subprocess.check_output(shlex.split(comando_remitente), stderr=subprocess.STDOUT)

        # Verificar si los directorios existen en la máquina destino
        comando_destino = f'ssh {usuario_remoto_destino}@{ip_remota_destino} test -d {directorio_destino}'
        subprocess.check_output(shlex.split(comando_destino), stderr=subprocess.STDOUT)

        return True
    except subprocess.CalledProcessError as e:
        # Puedes registrar el error en un log o manejarlo de alguna otra manera según tus necesidades
        return False

#ELIMINACION DE RESPALDOS (CRONS) DADOS DE ALTA
@require_http_methods(["GET", "POST"])
@login_required(login_url='/login/')
def ver_configuraciones_respaldo(request):
    configuraciones_respaldo = BackupConfig.objects.all()
    if request.method == 'POST':
        # obtiene los ids de para guardarlo en una variables y pasarlos como contexto
        configuracion_id = request.POST.get('configuracion_id', None)
        if configuracion_id:
            try:
                configuracion = BackupConfig.objects.get(id=configuracion_id)

                # Obtener el comentario almacenado en la base de datos
                comentario_db = configuracion.comment

                # Configurar el crontab
                my_cron = CronTab(user='hyper-lethal')

                # Buscar y eliminar la tarea con el comentario específico
                for job in my_cron:
                    if job.comment == comentario_db:
                        my_cron.remove(job)
                        my_cron.write()

                        # Eliminar de la base de datos
                        configuracion.delete()

                        messages.success(request, 'Configuración de respaldo eliminada correctamente.')
                        return redirect('/baja/')

                messages.warning(request, 'El comentario de la base de datos no está presente en el crontab.')

            except BackupConfig.DoesNotExist:
                messages.error(request, 'La configuración de respaldo no existe.')
                return redirect('/baja/')

    return render(request, 'baja.html', {'configuraciones_respaldo': configuraciones_respaldo})



#MUESTREO DE LOS CRONS EJECUTADOS
@require_http_methods(["GET"])
@login_required(login_url='/login/')
def cron_log_view(request):
    try:
        # Ejecuta el comando y filtrar las líneas que contienen "CRON" y el usuario del servidor "hyper-lethal"
        result = subprocess.run(['cat', '/var/log/syslog'], capture_output=True, text=True, check=True)
        log_lines = [line for line in result.stdout.splitlines() if "CRON" in line and "hyper-lethal" in line]

        # Crear un diccionario con la información formateada
        cron_log_content = {
            'total_lines': len(log_lines),
            'log_lines': log_lines
        }
    except subprocess.CalledProcessError as e:
        # Manejar errores en caso de haber un error 
        cron_log_content = {
            'error': f"Error al ejecutar el comando: {e}"
        }

    return render(request, 'cronlog.html', {'cron_log_content': cron_log_content})



#se ejecuta y se manda a llamar unicamente cuando el script se ejecute, cada 5 segundos

def ajax_cron_log(request):
    try:
        # Ejecutar el comando y filtrar las líneas que contienen "CRON" y "hyper-lethal"
        result = subprocess.run(['cat', '/var/log/syslog'], capture_output=True, text=True, check=True)
        cron_log_content = "\n".join(line for line in result.stdout.splitlines() if "CRON" in line and "hyper-lethal" in line)
    except subprocess.CalledProcessError as e:
        # Manejar errores al ejecutar el comando
        cron_log_content = f"Error al ejecutar el comando: {e}"

    return JsonResponse({'cron_log_content': cron_log_content})