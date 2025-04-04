import json
import os
from rag_engine import RAGEngine

# Inicializar el motor RAG (se cargará una sola vez durante cold start)
rag = RAGEngine()

def lambda_handler(event, context):
    """
    Función principal de AWS Lambda que procesa las solicitudes
    """
    try:
        # Extraer la consulta de los parámetros de la solicitud
        if 'queryStringParameters' in event and event['queryStringParameters'] and 'q' in event['queryStringParameters']:
            query = event['queryStringParameters']['q']
        else:
            # Si no hay query, usar body si existe
            body = json.loads(event.get('body', '{}')) if event.get('body') else {}
            query = body.get('query', '')
        
        # Si no hay query en ningún lado, devolver error
        if not query:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Se requiere un parámetro de consulta "q" o "query" en el body'
                })
            }
        
        # Determinar si usar RAG o matching simple basado en parámetros
        use_rag = True
        if 'queryStringParameters' in event and event['queryStringParameters'] and 'mode' in event['queryStringParameters']:
            if event['queryStringParameters']['mode'].lower() == 'simple':
                use_rag = False
        
        # Primero intentar con matching simple
        simple_answer = rag.simple_match(query)
        
        # Si hay una respuesta simple y no se requiere RAG, usarla
        if simple_answer and not use_rag:
            answer = simple_answer
        else:
            # Usar el motor RAG completo
            answer = rag.generate_answer(query, use_rag=use_rag)
        
        # Construir la respuesta
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'query': query,
                'answer': answer,
                'mode': 'rag' if use_rag else 'simple'
            })
        }
        
    except Exception as e:
        # Manejar errores
        print(f"Error procesando solicitud: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': f'Error interno: {str(e)}'
            })
        }

# Para ejecutar localmente para pruebas
if __name__ == "__main__":
    # Simular un evento de API Gateway
    test_event = {
        'queryStringParameters': {
            'q': '¿Qué es el QNH?'
        }
    }
    
    response = lambda_handler(test_event, None)
    print(json.dumps(response, indent=2)) 