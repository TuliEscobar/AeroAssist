# Optimización de AeroAssist para AWS Lambda

Este documento describe estrategias de optimización para ejecutar AeroAssist de manera eficiente como contenedor en AWS Lambda.

## Desafíos principales

1. **Tamaño del contenedor**: Lambda tiene un límite de 10GB para imágenes de contenedor
2. **Cold starts**: Los tiempos de arranque pueden afectar la experiencia de usuario
3. **Límites de memoria**: La carga de modelos de ML puede consumir mucha memoria
4. **Tiempo de ejecución**: Lambda tiene un límite máximo de ejecución (15 minutos)

## Estrategias de optimización implementadas

### 1. Optimización de la imagen Docker

- **Imagen base ligera**: Usamos `public.ecr.aws/lambda/python:3.11` que está optimizada para Lambda
- **Capas eficientes**: Ordenamos las capas Docker para maximizar el caché (dependencias primero)
- **Exclusión de archivos innecesarios**: No incluimos archivos de desarrollo (.git, tests, etc.)

### 2. Carga de modelos eficiente

- **Modelos más pequeños**: Elegimos modelos con buen balance rendimiento/tamaño:
  - `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (110MB) para embeddings
  - Modelos pequeños para la generación de texto (placeholder Falcon-7B-Instruct a reemplazar por uno más liviano)
- **Lazy loading**: El modelo generativo solo se carga cuando se necesita
- **Permanencia en memoria**: Los modelos permanecen cargados entre invocaciones

### 3. Optimización de recursos Lambda

- **Memoria suficiente**: Configuración recomendada de 2048-4096MB
- **Tiempo de espera adecuado**: Configurar al menos 30 segundos
- **Concurrencia aprovisionada**: Para casos de uso críticos, considerar la concurrencia aprovisionada para eliminar cold starts

### 4. Optimización de la base de conocimiento

- **Preprocessamiento**: Generación de embeddings al inicio para acelerar consultas
- **Umbral de confianza**: Solo se usa generación cuando es necesario
- **Índices eficientes**: Estructura optimizada para búsqueda rápida

## Pruebas y benchmarks

Para evaluar el rendimiento, ejecutar pruebas con diferentes configuraciones:

```bash
# Test de cold start
aws lambda invoke --function-name aeroassist --payload '{"queryStringParameters":{"q":"¿Qué es el QNH?"}}' response.json

# Test de concurrencia
ab -n 100 -c 10 https://tu-api.com/api?q=¿Qué%20es%20el%20QNH?
```

## Métricas a monitorear

- **Duración**: Tiempo de ejecución para responder a consultas
- **Cold start**: Tiempo de la primera ejecución
- **Memoria utilizada**: Uso máximo de memoria durante la ejecución
- **Error rate**: Tasa de errores en las respuestas

## Estrategias adicionales a considerar

1. **Distribución geográfica**: Desplegar en múltiples regiones para menor latencia
2. **Cuantización de modelos**: Reducir precisión de los pesos de modelos (FP16 o INT8)
3. **Caché de respuestas**: Almacenar respuestas comunes en una capa de caché (DynamoDB/ElastiCache)
4. **Distillation**: Usar modelos destilados que son más pequeños pero mantienen buen rendimiento
5. **Offloading**: Para consultas muy complejas, considerar delegarlas a un servicio específico

## Referencias

- [AWS Lambda Container Images Best Practices](https://aws.amazon.com/blogs/compute/best-practices-for-developing-on-aws-lambda/)
- [Optimizing Lambda Performance](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Sentence-Transformers Documentation](https://www.sbert.net/) 