# AeroAssist

Asistente virtual aeronáutico basado en AWS Lambda + IA, utilizando un enfoque RAG (Retrieval-Augmented Generation) con modelos de inteligencia artificial de código abierto.

## ¿Qué hace?

AeroAssist es un sistema que responde consultas técnicas y administrativas relacionadas con el sector aeronáutico, utilizando:

- Matching semántico mediante embeddings con `sentence-transformers`
- Base de conocimiento en formato JSON (faq_data.json)
- Opcionalmente, generación de respuestas con modelos como Falcon-7B-Instruct
- Arquitectura serverless en AWS Lambda mediante contenedores Docker

## Componentes principales

- `app.py`: punto de entrada para AWS Lambda
- `rag_engine.py`: motor de búsqueda y generación con enfoque RAG
- `faq_data.json`: base de conocimiento aeronáutico
- `Dockerfile`: definición del contenedor
- `entry.sh`: script de entrada para el contenedor Lambda
- `requirements.txt`: dependencias del proyecto

## Cómo usar

### Despliegue local (para pruebas)

1. Clonar este repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar `python app.py` para probar localmente

### Despliegue en AWS Lambda (producción)

#### 1. Construir la imagen de Docker

```bash
# Autenticarse en AWS ECR
aws ecr get-login-password --region <tu-region> | docker login --username AWS --password-stdin <cuenta-aws>.dkr.ecr.<tu-region>.amazonaws.com

# Crear repositorio en ECR (si no existe)
aws ecr create-repository --repository-name aeroassist --image-scanning-configuration scanOnPush=true

# Construir la imagen
docker build -t aeroassist:latest .

# Etiquetar la imagen para ECR
docker tag aeroassist:latest <cuenta-aws>.dkr.ecr.<tu-region>.amazonaws.com/aeroassist:latest

# Subir la imagen a ECR
docker push <cuenta-aws>.dkr.ecr.<tu-region>.amazonaws.com/aeroassist:latest
```

#### 2. Crear función Lambda

1. Ir a la consola de AWS Lambda
2. Crear nueva función
3. Seleccionar "Container image" como origen
4. Elegir la imagen de ECR recién subida
5. Configurar:
   - Memoria: mínimo 2048 MB (recomendado 4096 MB)
   - Tiempo de espera: 30 segundos o más
   - Variables de entorno: configura según necesidades

#### 3. Configurar API Gateway

1. Crear API REST en API Gateway
2. Crear recurso y método (GET)
3. Integrar con la función Lambda
4. Desplegar API

## Ejemplos de uso

### Modo simple (matching directo)

```
https://tu-api.com/api?q=¿Qué es el QNH?&mode=simple
```

### Modo RAG (generación aumentada)

```
https://tu-api.com/api?q=¿Qué debo hacer si hay turbulencia?
```

## Optimizaciones

- El modelo de embeddings se carga una sola vez durante el inicio "cold start"
- El modelo generativo se carga bajo demanda (lazy loading)
- Versiones específicas de las dependencias para evitar conflictos
- Configuración optimizada para contenedores Lambda

## Desarrollo

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama de características (`git checkout -b feature/nueva-caracteristica`)
3. Commit de cambios (`git commit -am 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## Licencia

MIT