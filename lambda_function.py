import json

def load_faqs():
    with open("faq_data.json", encoding="utf-8") as f:
        return json.load(f)

def match_question(user_question, faqs):
    for item in faqs:
        if item["question"].lower() in user_question.lower():
            return item["answer"]
    return None

def lambda_handler(event, context):
    question = event.get("queryStringParameters", {}).get("q", "")
    faqs = load_faqs()
    
    answer = match_question(question, faqs)
    if not answer:
        answer = "Lo siento, no tengo una respuesta exacta. ¿Querés que consulte al sistema de IA?"

    return {
        "statusCode": 200,
        "body": json.dumps({
            "question": question,
            "answer": answer
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }