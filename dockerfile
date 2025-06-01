# 1. Usar una imagen base de Python delgada
FROM python:3.9-slim

# 2. Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Establecer el directorio de trabajo DENTRO del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema operativo para mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar SOLO el archivo de requerimientos primero
COPY requirements.txt .

# 6. Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiar TODO el resto de tu proyecto al directorio /app del contenedor
COPY . .

# 8. Exponer el puerto en el que Gunicorn escuchará DENTRO del contenedor
EXPOSE 8000

# 9. Comando para ejecutar la aplicación con Gunicorn.
# 'proy.wsgi:application' debe coincidir con el nombre de tu proyecto Django.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "proy.wsgi:application"
