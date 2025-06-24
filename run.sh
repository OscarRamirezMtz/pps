#!/usr/bin/env bash

# 
echo "Esperando a que la base de datos se inicie..."
sleep 15 #

echo "Ejecutando makemigrations..."
python -u manage.py makemigrations backend #

sleep 5

echo "Ejecutando migraciones..."
python -u manage.py migrate --noinput

#echo "Recolectando archivos estáticos..."
#python -u manage.py collectstatic --noinput --clear 

echo "Iniciando Gunicorn..."

# Quita --reload para producción
#gunicorn --reload --bind 0.0.0.0:8000 proy.wsgi:application #desarrollo
gunicorn --bind 0.0.0.0:8000 proy.wsgi:application #produccion
