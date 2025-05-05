import subprocess

def envio():
    ip = ''
    directorio_local = ''
    directorio_des = ''


    try:
        command = f"rsync -avz -e ssh {directorio_local} {ip}:{directorio_des}"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(f"Resultado: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")

# Uso de la función
envio()