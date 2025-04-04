#!/bin/bash

# Script de despliegue para AeroAssist en AWS Lambda
# ----------------------------------------------

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=== AeroAssist - Script de Despliegue ===${NC}"
echo -e "Este script automatiza el despliegue de AeroAssist como contenedor en AWS Lambda"
echo -e "${YELLOW}Requisitos: AWS CLI configurado, Docker instalado${NC}"
echo

# Solicitar datos de configuración
read -p "Región AWS (ej. us-east-1): " AWS_REGION
read -p "Nombre del repositorio ECR (default: aeroassist): " ECR_REPO
ECR_REPO=${ECR_REPO:-aeroassist}

# Obtener ID de cuenta AWS
echo -e "${CYAN}Obteniendo ID de cuenta AWS...${NC}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]; then
    echo -e "${RED}Error al obtener ID de cuenta AWS. Verifica que AWS CLI esté configurado correctamente.${NC}"
    exit 1
fi

echo -e "ID de cuenta AWS: ${AWS_ACCOUNT_ID}"

# Configurar rutas ECR
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
ECR_REPOSITORY="${ECR_URI}/${ECR_REPO}"

# Paso 1: Autenticación en ECR
echo -e "\n${CYAN}[1/5] Autenticando en AWS ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

if [ $? -ne 0 ]; then
    echo -e "${RED}Error de autenticación en ECR.${NC}"
    exit 1
fi

# Paso 2: Crear repositorio ECR si no existe
echo -e "\n${CYAN}[2/5] Verificando/creando repositorio ECR...${NC}"
aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Repositorio no encontrado. Creando repositorio '${ECR_REPO}'...${NC}"
    aws ecr create-repository --repository-name $ECR_REPO --image-scanning-configuration scanOnPush=true --region $AWS_REGION
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error al crear el repositorio ECR.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Repositorio '$ECR_REPO' ya existe.${NC}"
fi

# Paso 3: Construir imagen Docker
echo -e "\n${CYAN}[3/5] Construyendo imagen Docker...${NC}"
docker build -t $ECR_REPO:latest .

if [ $? -ne 0 ]; then
    echo -e "${RED}Error al construir la imagen Docker.${NC}"
    exit 1
fi

# Paso 4: Etiquetar y subir imagen a ECR
echo -e "\n${CYAN}[4/5] Etiquetando y subiendo imagen a ECR...${NC}"
docker tag $ECR_REPO:latest $ECR_REPOSITORY:latest
echo -e "Imagen etiquetada como $ECR_REPOSITORY:latest"

echo -e "${YELLOW}Subiendo imagen a ECR (esto puede tardar un tiempo)...${NC}"
docker push $ECR_REPOSITORY:latest

if [ $? -ne 0 ]; then
    echo -e "${RED}Error al subir la imagen a ECR.${NC}"
    exit 1
fi

# Paso 5: Instrucciones para crear la función Lambda
echo -e "\n${CYAN}[5/5] Configuración de Lambda...${NC}"
echo -e "${GREEN}¡Imagen subida exitosamente a ECR!${NC}"
echo 
echo -e "${CYAN}Instrucciones para crear la función Lambda:${NC}"
echo -e "1. Ve a la consola AWS Lambda: https://${AWS_REGION}.console.aws.amazon.com/lambda/home?region=${AWS_REGION}#/functions"
echo -e "2. Haz clic en 'Crear función'"
echo -e "3. Selecciona 'Imagen de contenedor'"
echo -e "4. Nombre de función: ${ECR_REPO}"
echo -e "5. URI de imagen de contenedor: ${ECR_REPOSITORY}:latest"
echo -e "6. Arquitectura: x86_64"
echo -e "7. Asigna memoria recomendada: 2048 MB (o más)"
echo -e "8. Configura tiempo de espera mayor a 30 segundos"
echo -e "9. Haz clic en 'Crear función'"
echo
echo -e "${YELLOW}Nota:${NC} Recuerda configurar un desencadenador (API Gateway) después de crear la función"
echo -e "${GREEN}¡Despliegue completado correctamente!${NC}" 