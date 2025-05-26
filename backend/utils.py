import random
import string
import requests
import os

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