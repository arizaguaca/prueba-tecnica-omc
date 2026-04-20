from openai import OpenAI
from app.core.config import settings
from typing import List, Dict
import json

class AIService:
    @staticmethod
    def generate_summary(leads_data: List[Dict]) -> Dict:
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_api_key_here":
            return {
                "summary": "Resumen Mock: Se observa un crecimiento sostenido en la captación de leads.",
                "analysis": "El análisis muestra que la mayoría de los interesados buscan soluciones de consultoría.",
                "best_source": "Instagram (Mock)",
                "marketing_recommendations": [
                    "Aumentar la inversión en Ads de Meta.",
                    "Optimizar la landing page para dispositivos móviles.",
                    "Implementar campañas de retargeting por email."
                ],
                "is_mock": True
            }

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Prepare data for LLM
        formatted_leads = [
            {
                "nombre": l["nombre"],
                "email": l["email"],
                "fuente": l["fuente"],
                "producto": l["producto_interes"],
                "presupuesto": l["presupuesto"]
            }
            for l in leads_data
        ]

        prompt = f"""
        Actúa como un experto en marketing y análisis de datos. 
        Analiza los siguientes datos de leads y genera un resumen ejecutivo en formato JSON.
        
        Datos de los leads:
        {json.dumps(formatted_leads, indent=2)}
        
        El JSON debe tener exactamente estas llaves:
        - summary: Análisis general de los leads.
        - analysis: Análisis detallado del comportamiento.
        - best_source: Cuál es la fuente que más convierte o tiene mejores leads.
        - marketing_recommendations: Lista de 3 recomendaciones estratégicas.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {{"role": "system", "content": "Eres un asistente experto en marketing que responde siempre en formato JSON."}},
                    {{"role": "user", "content": prompt}}
                ],
                response_format={{ "type": "json_object" }}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {{
                "error": f"Error calling OpenAI: {{str(e)}}",
                "is_mock": False
            }}
