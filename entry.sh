#!/bin/bash

# Script de entrada para el contenedor Lambda de AeroAssist
# Este script es llamado por el runtime de Lambda al iniciar el contenedor

# Llamar al handler del runtime de Python en AWS Lambda
# El formato es: <nombre_archivo>.<nombre_función>
exec python -m awslambdaric app.lambda_handler 