# AeroAssist FAQs Chatbot 🛩️

Un chatbot inteligente que responde preguntas sobre regulaciones aeronáuticas utilizando la API de Google Gemini.

## Características ✨

- Utiliza el modelo Gemini de Google para respuestas precisas
- Base de conocimiento en formato JSON para FAQs
- Respuestas contextualizadas basadas en preguntas frecuentes
- Interfaz de línea de comandos intuitiva

## Requisitos 📋

- Python 3.8+
- Cuenta de Google Cloud con API key para Gemini
- Archivo `.env` con las credenciales necesarias

## Instalación 🚀

1. Clonar el repositorio:
```bash
git clone https://github.com/TuliEscobar/AeroAssist.git
cd AeroAssist
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Crear archivo `.env` con tu API key:
```
GOOGLE_API_KEY=tu_api_key_aqui
```

## Uso 💻

1. Asegúrate de tener un archivo `faqs.json` con el siguiente formato:
```json
[
    {
        "pregunta": "¿Pregunta sobre regulación?",
        "respuesta": "Respuesta detallada..."
    }
]
```

2. Ejecutar el programa:
```bash
python main.py
```

3. Hacer preguntas sobre regulaciones aeronáuticas o escribir 'salir' para terminar.

## Estructura del Proyecto 📁

```
AeroAssist_faqsChatbot_v1/
├── main.py           # Archivo principal del chatbot
├── faqs.json        # Base de conocimiento
├── .env            # Configuración de variables de entorno
└── requirements.txt # Dependencias del proyecto
```

## Contribuir 🤝

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abrir un Pull Request

## Licencia 📄

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor ✒️

* **Tuli Escobar** - [TuliEscobar](https://github.com/TuliEscobar) 