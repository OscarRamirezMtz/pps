# import random
# import string

# def generate_otp(length=6):
#     return ''.join(random.choices(string.digits, k=length))

# import requests


# def mandar_mensaje(mensaje: str, token=TOKEN, chat_id=CHAT_ID) -> bool:
#     url = f'https://api.telegram.org/bot{token}/sendMessage'
#     data = {
#         'chat_id': chat_id,
#         'text': mensaje,
#         'parse_mode': 'Markdown'
#     }
#     try:
#         response = requests.post(url, data=data)
#         return response.status_code == 200
#     except Exception as e:
#         print("Error enviando mensaje:", e)
#         return False
