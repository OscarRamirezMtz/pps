# 1. Imagen base de Python actualizada a 3.11
FROM python:3.11

# 2. Variables de entorno para Python

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar el archivo de requerimientos e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo el código del proyecto al directorio de trabajo /app
COPY . .

# 7. Copiar el script de ejecución y darle permisos
COPY run.sh /run.sh
RUN chmod +x /run.sh

# 8. Exponer el puerto en el que Gunicorn se ejecutará (interno al contenedor)
EXPOSE 8000

# 9. Comando para ejecutar la aplicación
# Esto será ejecutado por el script run.sh
ENTRYPOINT ["/run.sh"]
