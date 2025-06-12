from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← NUEVA LÍNEA
import unicodedata
import requests
import json

app = FastAPI(title="Sistema de Agentes Inteligentes")

# CONFIGURACIÓN CORS - AGREGA ESTO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def quitar_acentos(texto):
    """Quita acentos y normaliza el texto"""
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_acentos = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
    return texto_sin_acentos.lower()

def contiene_alguna(texto, lista_palabras):
    texto_limpio = quitar_acentos(texto)
    for palabra in lista_palabras:
        palabra_limpia = quitar_acentos(palabra)
        if palabra_limpia in texto_limpio:
            return True
    return False

# AGENTE 1: Experto Inmobiliario INTELIGENTE
@app.get("/agente-inmobiliario-smart/{pregunta}")
def agente_inmobiliario_smart(pregunta: str):
    pregunta_lower = pregunta.lower()
    
    palabras_donde = ["donde", "ubicacion", "zona", "lugar", "area", "barrio", "sector"]
    palabras_cuanto = ["cuanto", "precio", "costo", "dinero", "presupuesto", "capital"]
    palabras_como = ["como", "estrategia", "forma", "manera", "proceso", "pasos"]
    palabras_cuando = ["cuando", "tiempo", "momento", "fecha", "plazo"]
    
    if contiene_alguna(pregunta_lower, palabras_donde):
        return {
            "agente": "Consultor Inmobiliario Senior",
            "tema_detectado": "Ubicación/Dónde",
            "respuesta": "Zonas recomendadas: 1) Centros urbanos en regeneración, 2) Cerca de universidades, 3) Proyectos de metro/transporte, 4) Barrios emergentes.",
            "tip_extra": "Investiga planes municipales de desarrollo urbano.",
            "riesgo": "Medio-Bajo"
        }
        
    elif contiene_alguna(pregunta_lower, palabras_cuanto):
        return {
            "agente": "Consultor Inmobiliario Senior", 
            "tema_detectado": "Presupuesto/Cuánto",
            "respuesta": "Máximo 30% de ingresos mensuales. Reserva de emergencia: 6-12 meses de gastos.",
            "formula": "Ingreso mensual × 0.30 = Cuota máxima",
            "tip_extra": "Considera gastos adicionales: impuestos, mantenimiento, seguros."
        }
        
    elif contiene_alguna(pregunta_lower, palabras_como):
        return {
            "agente": "Consultor Inmobiliario Senior",
            "tema_detectado": "Estrategia/Cómo",
            "respuesta": "Pasos: 1) Define presupuesto, 2) Investiga mercado, 3) Analiza ubicación, 4) Evalúa rentabilidad, 5) Negocia precio.",
            "tip_clave": "Siempre inspecciona físicamente antes de comprar"
        }
        
    elif contiene_alguna(pregunta_lower, palabras_cuando):
        return {
            "agente": "Consultor Inmobiliario Senior",
            "tema_detectado": "Timing/Cuándo",
            "respuesta": "Mejor momento: cuando tengas estabilidad financiera + fondo de emergencia + al menos 20% de enganche.",
            "indicadores": "Mercado en crecimiento moderado, tasas de interés estables"
        }
        
    else:
        return {
            "agente": "Consultor Inmobiliario Senior",
            "mensaje": f"No reconozco el tema en '{pregunta}'. ¿Preguntas sobre DÓNDE, CUÁNTO, CÓMO o CUÁNDO invertir?",
            "sugerencias": ["donde invertir", "cuanto dinero necesito", "como empezar", "cuando comprar"]
        }

# AGENTE 2: Analista Financiero INTELIGENTE
@app.get("/agente-financiero-smart/{pregunta}")  
def agente_financiero_smart(pregunta: str):
    pregunta_lower = pregunta.lower()
    
    palabras_ahorro = ["ahorro", "ahorrar", "ahorros", "guardando", "guardar dinero", "reservar"]
    palabras_inversion = ["invertir", "inversion", "inversiones", "rentabilidad", "ganancias"]
    
    if contiene_alguna(pregunta_lower, palabras_ahorro):
        return {"agente": "Experto Financiero", "tema_detectado": "Ahorro", "respuesta": "Regla 50/30/20: 50% gastos necesarios, 30% personales, 20% ahorro/inversión"}
        
    elif contiene_alguna(pregunta_lower, palabras_inversion):
        return {"agente": "Experto Financiero", "tema_detectado": "Inversión", "respuesta": "Diversificación: 60% acciones, 30% bonos, 10% alternativos"}
        
    else:
        return {"agente": "Experto Financiero", "mensaje": f"No reconozco '{pregunta}'. ¿Hablas de ahorro o inversión?"}

def detectar_tema(pregunta):
    if any(palabra in pregunta.lower() for palabra in ["invert", "propied", "inmuebl"]):
        return "inversiones inmobiliarias"
    elif any(palabra in pregunta.lower() for palabra in ["ahorr", "financ", "diner"]):
        return "finanzas personales"
    return "consultoría general"

def generar_respuesta_experta(pregunta):
    tema = detectar_tema(pregunta)
    if "inmobiliarias" in tema:
        return "Analiza ubicación estratégica, potencial de valorización y flujo de caja positivo. ROI objetivo: 8-15% anual."
    elif "finanzas" in tema:
        return "Implementa regla 50/30/20, crea fondo de emergencia y diversifica inversiones según tu perfil de riesgo."
    return "Define objetivos claros, analiza opciones disponibles y toma decisiones basadas en datos."

# AGENTE 3: IA REAL con Groq
@app.get("/agente-ia-real/{pregunta}")
def agente_ia_real(pregunta: str):
    
    import os
# ... (tus otros imports)

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Eres un consultor financiero experto, amigable y conversacional. Responde como si fueras un asesor humano experimentado. Explica de forma clara y práctica, dando ejemplos específicos. Responde en español de manera cálida y profesional."},
            {"role": "user", "content": pregunta}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        return {
            "pregunta": pregunta,
            "respuesta": result["choices"][0]["message"]["content"],
            "modelo": "Mixtral-8x7B (Groq)",
            "estado": "IA Real Activa"
        }
        
    except Exception as e:
        return {
            "pregunta": pregunta,
            "respuesta": f"Error de conexión. Respuesta local: {generar_respuesta_experta(pregunta)}",
            "error": str(e)
        }
