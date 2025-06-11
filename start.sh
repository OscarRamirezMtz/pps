#!/usr/bin/env bash

while read -r linea; do    
    export "$linea"
done < <(ccdecrypt -c secreto.env.cpt)

docker-compose up --build

