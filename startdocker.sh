#!/usr/bin/env bash

# Nombre del archivo cifrado
ENCRYPTED_FILE="secreto.env.cpt" # Asegúrate que este sea el nombre correcto

# Pedir la contraseña de forma segura
echo -n "Ingresa la contraseña para descifrar los secretos: "
read -s PASSWORD
echo # Nueva línea

# Intentar descifrar el archivo y exportar las variables
# La salida de ccdecrypt se procesa línea por línea
echo "Descifrando y exportando secretos a variables de entorno..."
DECRYPTED_CONTENT=$(echo "$PASSWORD" | ccdecrypt -c -k "" "$ENCRYPTED_FILE" 2>/dev/null)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ] && [ -n "$DECRYPTED_CONTENT" ]; then
    echo "$DECRYPTED_CONTENT" | while IFS= read -r linea || [ -n "$linea" ]; do
        linea_limpia=$(echo "$linea" | awk '{$1=$1};1') # Limpiar espacios
        if [ -n "$linea_limpia" ]; then
            export "$linea_limpia" # Exporta la variable al entorno actual del script
            # echo "Exportado: $linea_limpia" # Descomentar para depurar
        fi
    done
    echo "Secretos exportados al entorno del shell."

    # Limpiar la contraseña de la memoria del script (opcional, pero buena práctica)
    unset PASSWORD
    unset DECRYPTED_CONTENT

    echo "Levantando contenedores Docker con 'docker-compose up --build'..."
    echo "Presiona Ctrl+C para detener los contenedores."

    # Ejecutar docker-compose. Ahora leerá las variables exportadas del entorno.
    docker-compose up --build

    echo "Proceso de Docker Compose finalizado."

else
    echo "Error: Falló el descifrado. Verifica la contraseña."
    unset PASSWORD # Limpiar la contraseña
    exit 1
fi
