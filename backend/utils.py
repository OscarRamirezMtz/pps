import string
import requests
import os
import paramiko
import secrets
from django.conf import settings
from pathlib import Path 
from django.conf import settings
from pathlib import Path

def generate_otp(length=8):
    return ''.join(secrets.choice(string.digits) for _ in range(length))

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
MASTER_KEY = os.environ.get('MASTER_KEY')

def mandar_mensaje(mensaje: str, token=TOKEN, chat_id=CHAT_ID) -> bool:
    """Envia el codigo OTP por medio de Telegram
    """
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
    
def ejecutar_comando_remoto(servidor, comando):
    """
    Se conecta usando la llave SSH
    y ejecuta un comando con sudo, asumiendo que la regla NOPASSWD ya existe.
    """
    resultado = {'stdout': '', 'stderr': '', 'exit_code': -1, 'error_conexion': None}
    ssh_client = None
    try:
        master_key_passphrase = settings.MASTER_KEY
        if not master_key_passphrase:
            raise ValueError("MASTER_ENCRYPTION_KEY no está definida.")

        key_filepath = Path(settings.BASE_DIR) / '.ssh_keys' / 'app_id_rsa'
        with open(key_filepath) as key_file:
            private_key = paramiko.RSAKey.from_private_key(key_file, password=master_key_passphrase)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=servidor.direccion_host, port=servidor.ssh_port,
            username=servidor.usuario_remoto, pkey=private_key, timeout=10
        )
        
        # Ejecuta el comando asumiendo que NOPASSWD está configurado
        stdin, stdout, stderr = ssh_client.exec_command(f"sudo {comando}")
        
        resultado.update({
            'stdout': stdout.read().decode('utf-8').strip(),
            'stderr': stderr.read().decode('utf-8').strip(),
            'exit_code': stdout.channel.recv_exit_status()
        })
    except Exception as e:
        resultado['error_conexion'] = str(e)
    finally:
        if ssh_client:
            ssh_client.close()
    return resultado
