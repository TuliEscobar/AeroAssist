import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-1.5-pro-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"



def cargar_faqs(ruta='faqs.json'):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def construir_contexto(faqs):
    return "\n".join([f"P: {faq['pregunta']}\nR: {faq['respuesta']}" for faq in faqs])


def preguntar_al_modelo(pregunta, contexto):
    headers = {"Content-Type": "application/json"}

    prompt = f"{contexto}\n\nPregunta: {pregunta}\nRespuesta:"

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        mensaje = response.json()
        return mensaje['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"


if __name__ == "__main__":
    faqs = cargar_faqs()
    contexto = construir_contexto(faqs)

    while True:
        pregunta = input("\nHaz una pregunta sobre regulaciones aeronáuticas (o 'salir'): ")
        if pregunta.lower() == 'salir':
            break
        respuesta = preguntar_al_modelo(pregunta, contexto)
        print(f"\n✈️ Respuesta: {respuesta}")
