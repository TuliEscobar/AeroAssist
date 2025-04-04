import json
import os
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

class RAGEngine:
    def __init__(self, faq_path="faq_data.json", model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """Inicializa el motor RAG con embeddings y fuentes de conocimiento"""
        self.faq_data = self._load_faqs(faq_path)
        
        # Cargar el modelo de embeddings
        self.embedding_model = SentenceTransformer(model_name)
        
        # Procesar los FAQs para crear embeddings
        self.processed_faqs = self._process_faqs()
        
        # Modelo de generación (inicialización perezosa cuando se necesite)
        self.generation_model = None
        self.tokenizer = None

    def _load_faqs(self, path):
        """Carga los datos de FAQ desde un archivo JSON"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando FAQs: {e}")
            # Fallback a un FAQ básico si hay error
            return [{"question": "¿Qué es AeroAssist?", 
                    "answer": "AeroAssist es un asistente virtual para consultas aeronáuticas."}]
    
    def _process_faqs(self):
        """Procesa los FAQs para generar embeddings"""
        processed = []
        
        for item in self.faq_data:
            # Crear embedding para cada pregunta
            embedding = self.embedding_model.encode(item["question"])
            
            processed.append({
                "question": item["question"],
                "answer": item["answer"],
                "embedding": embedding
            })
        
        return processed
    
    def _load_generation_model(self):
        """Carga el modelo de generación de texto bajo demanda"""
        if self.generation_model is None:
            # Usar un modelo más liviano compatible con Lambda
            model_name = "Falcon-7B-Instruct" # Este es un placeholder, usar un modelo realmente liviano
            
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.generation_model = AutoModelForCausalLM.from_pretrained(
                    model_name, 
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True,
                    device_map="auto"
                )
            except Exception as e:
                print(f"Error cargando modelo generativo: {e}")
                return False
        return True
    
    def find_best_match(self, query, top_k=3, threshold=0.6):
        """Encuentra las mejores coincidencias para una consulta usando similitud coseno"""
        query_embedding = self.embedding_model.encode(query)
        
        similarities = []
        for item in self.processed_faqs:
            # Calcular similitud coseno
            similarity = np.dot(query_embedding, item["embedding"]) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(item["embedding"])
            )
            similarities.append((item, similarity))
        
        # Ordenar por similitud (mayor a menor)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filtrar por umbral y obtener los top_k
        best_matches = [item for item, score in similarities[:top_k] if score >= threshold]
        
        return best_matches
    
    def generate_answer(self, query, use_rag=True):
        """Genera una respuesta basada en la consulta, opcionalmente usando RAG"""
        # Primero buscar coincidencias en el FAQ
        matches = self.find_best_match(query)
        
        # Si hay coincidencias buenas, usar la respuesta directamente
        if matches and not use_rag:
            return matches[0]["answer"]
        
        # Si queremos RAG, combinar conocimiento y generar respuesta
        if use_rag:
            # Solo cargar el modelo generativo si es necesario
            if not self._load_generation_model():
                # Fallback si no se puede cargar el modelo
                return matches[0]["answer"] if matches else "No puedo procesar esa consulta en este momento."
            
            # Generar un contexto basado en las coincidencias
            context = ""
            if matches:
                for idx, match in enumerate(matches):
                    context += f"Info {idx+1}: {match['question']}: {match['answer']}\n"
            
            # Crear el prompt para el modelo generativo
            prompt = f"""
            Eres un asistente aeronáutico profesional. Responde a la siguiente consulta 
            usando solo el contexto proporcionado si es relevante.
            
            Contexto:
            {context}
            
            Consulta: {query}
            
            Respuesta concisa y profesional:
            """
            
            # Generar respuesta
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.generation_model.device)
            output = self.generation_model.generate(
                inputs["input_ids"],
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True
            )
            
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            return response.split("Respuesta concisa y profesional:")[-1].strip()
        
        # Si no hay coincidencias y no usamos RAG
        return "No tengo información específica sobre esa consulta aeronáutica."
        
    def simple_match(self, query):
        """Método simple para hacer matching directo de preguntas"""
        for item in self.faq_data:
            if item["question"].lower() in query.lower():
                return item["answer"]
        return None 