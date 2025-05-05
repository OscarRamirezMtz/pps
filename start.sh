#!/usr/bin/env bash

while read -r linea; do    
    export "$linea"
done < <(ccdecrypt -c secreto.env.cpt)
#python manage.py runserver
if [ $# -eq 0 ]; then
    python manage.py runserver
else
    python manage.py "$@"
fi
