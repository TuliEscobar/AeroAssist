# Presentación AeroAssist - Hackathon Serverless Guru

## Equipo
- Héctor - Desarrollador Backend / Ex Controlador de Tránsito Aéreo / Estudiante de IA

## Problema a resolver

En el sector aeronáutico existe un gran volumen de consultas técnicas y administrativas que suelen ser repetitivas pero críticas. Actualmente:

- Los operadores aeronáuticos dedican mucho tiempo a responder preguntas frecuentes
- La información técnica está dispersa y a veces es difícil de acceder
- Las respuestas deben ser precisas debido a la naturaleza crítica de la aviación
- La información debe estar disponible de forma inmediata

## Solución: AeroAssist

AeroAssist es un asistente virtual especializado en aeronáutica que:

- Responde consultas técnicas y administrativas de forma precisa
- Utiliza IA para entender preguntas y proporcionar respuestas contextualizadas
- Está siempre disponible (24/7) gracias a arquitectura serverless
- Es económico de operar gracias a modelos de lenguaje abiertos y eficientes
- Puede escalar según demanda sin degradar su rendimiento

## Arquitectura

- **Frontend**: Interfaz simple web/móvil (simulada para demo)
- **API Gateway**: Punto de entrada REST
- **AWS Lambda**: Contenedor Docker con toda la lógica
- **RAG Engine**: Retrieval-Augmented Generation con embeddings semánticos
- **Modelos open-source**: Sentence-transformers + Falcon-7B-Instruct
- **Base de conocimiento**: Datos estructurados en formato JSON (extensible)

## Tecnologías utilizadas

- **AWS Lambda**: Computación serverless
- **Docker**: Contenedorización
- **Python**: Lenguaje de programación principal
- **Sentence-transformers**: Embeddings semánticos multilingües
- **Modelos transformers**: Generación de texto contextual
- **AWS ECR**: Repositorio de contenedores

## Demo en vivo

1. Consulta simple: ¿Qué es el QNH?
2. Consulta compleja: ¿Cómo afecta la altitud de densidad al rendimiento de una aeronave?
3. Consulta no prevista: Adaptación con contexto de la base de conocimiento

## Ventajas del enfoque serverless

- **Pago por uso**: Solo se paga por el tiempo de ejecución
- **Escalabilidad**: Sin preocupaciones por la infraestructura
- **Mantenimiento mínimo**: Sin servidores que administrar
- **Disponibilidad**: Alta disponibilidad inherente

## Posibles mejoras futuras

- Integración con chatbots (Telegram, WhatsApp)
- Base de conocimiento expandida con documentos técnicos completos
- Fine-tuning de modelos específicos para terminología aeronáutica
- Interfaces de voz para uso en cabina o torre de control
- Soporte para múltiples idiomas con detección automática

## Valor para la industria aeronáutica

- **Reducción de costos**: Menos personal dedicado a responder consultas básicas
- **Disponibilidad constante**: Información crítica disponible 24/7
- **Consistencia**: Respuestas estandarizadas y precisas
- **Accesibilidad**: Democratiza el acceso a información técnica
- **Escalabilidad**: Puede atender desde un aeropuerto pequeño hasta una aerolínea internacional

## Gracias

Preguntas y respuestas 