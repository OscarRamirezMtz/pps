import random
import string
import requests
import os
import paramiko
from backend.models import Servidor

def generate_otp(length=8):
    return ''.join(random.choices(string.digits, k=length))

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def mandar_mensaje(mensaje: str, token=TOKEN, chat_id=CHAT_ID) -> bool:
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print("Error enviando mensaje:", e)
        return False



def ejecutar_comando_ssh(servidor_obj: Servidor, comando: str) -> tuple[bool, str, str, int]:
    """
    Se conecta a un servidor vía SSH y ejecuta un comando.
    Retorna (exito_conexion: bool, stdout: str, stderr: str, exit_status: int | None).
    exit_status es el código de salida del comando, o None si la conexión falló antes.
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    stdout_str = ""
    stderr_str = ""
    exit_status = -1 # Código de salida por defecto para error de conexión/setup

    try:
        # print(f"DEBUG: Conectando a {servidor_obj.direccion_host}:{servidor_obj.ssh_port} como {servidor_obj.usuario_remoto}")
        # print(f"DEBUG: Ejecutando comando: {comando}")

        # Para producción, considera rutas explícitas a claves o un agente SSH seguro.
        # Paramiko buscará claves en ~/.ssh/id_rsa, ~/.ssh/id_dsa etc., y usará el agente SSH si está disponible.
        ssh_client.connect(
            hostname=servidor_obj.direccion_host,
            port=servidor_obj.ssh_port,
            username=servidor_obj.usuario_remoto,
            timeout=10, # Tiempo de espera para la conexión en segundos
            allow_agent=True, # Intenta usar el agente SSH
            look_for_keys=True # Busca claves SSH locales conocidas
            # key_filename='/ruta/a/tu/clave_privada_especifica' # Descomenta y usa si tienes una clave no estándar
        )
        
        stdin, stdout, stderr = ssh_client.exec_command(comando, timeout=20) # Timeout para la ejecución del comando
        
        # Esperar a que el comando termine y obtener el código de salida
        exit_status = stdout.channel.recv_exit_status() 
        
        # Leer la salida estándar y de error
        stdout_str = stdout.read().decode('utf-8', errors='replace').strip()
        stderr_str = stderr.read().decode('utf-8', errors='replace').strip()
        
        # print(f"DEBUG: Comando ejecutado. Exit status: {exit_status}")
        # print(f"DEBUG: STDOUT: {stdout_str}")
        # print(f"DEBUG: STDERR: {stderr_str}")
        
        # El éxito de la ejecución del comando depende del exit_status
        return True, stdout_str, stderr_str, exit_status

    except paramiko.AuthenticationException:
        error_msg = "Error de autenticación SSH. Verifica el usuario, la clave SSH o la configuración del servidor."
        # print(f"DEBUG: {error_msg}")
        return False, "", error_msg, None # None para exit_status si la conexión falló
    except paramiko.SSHException as ssh_ex:
        error_msg = f"Error en la conexión SSH: {str(ssh_ex)}"
        # print(f"DEBUG: {error_msg}")
        return False, "", error_msg, None
    except TimeoutError: # Captura TimeoutError de socket
        error_msg = "Timeout durante la conexión o ejecución del comando SSH."
        # print(f"DEBUG: {error_msg}")
        return False, "", error_msg, None
    except Exception as e:
        error_msg = f"Error inesperado en la ejecución SSH: {str(e)}"
        # print(f"DEBUG: {error_msg}")
        return False, "", error_msg, None
    finally:
        if ssh_client:
            ssh_client.close()