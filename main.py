from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import unicodedata
import requests
import json

app = FastAPI(title="Sistema de Agentes Inteligentes")

# CONFIGURACIÓN CORS 
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


@app.get("/")
async def home():
    return {"message": "Sistema de Agentes IA - API activa"}
    
# 1. CONFIGURACIÓN CENTRALIZADA
PROMPTS_AGENTES = {
    "inmobiliario": "Eres un consultor inmobiliario experto...",
    "financiero": "Eres un asesor financiero senior...",
    "tecnologia": "Eres un CTO con 15 años de experiencia...",
    "negocios": "Eres un consultor de negocios estratégico...",
    "general": "Eres un asistente IA versátil y experto..."
}

# 2. FUNCIÓN GENÉRICA 
def consultar_agente_ia(pregunta: str, tipo_agente: str):
    
    # Validación
    if tipo_agente not in PROMPTS_AGENTES:
        return {"error": "Tipo de agente no válido"}
    
    # Configuración API
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    url = "https://api.deepseek.com/v1/chat/completions"
    
    # Headers 
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Data (solo cambiamos el prompt)
    data = {
        "model": "deepseek-reasoner",
        "messages": [
            {"role": "system", "content": PROMPTS_AGENTES[tipo_agente]},
            {"role": "user", "content": pregunta}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    # API Call 
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        return {
            "pregunta": pregunta,
            "respuesta": result["choices"][0]["message"]["content"],
            "agente": tipo_agente,
            "modelo": "deepseek-reasoner"
        }
    except Exception as e:
        return {
            "pregunta": pregunta,
            "error": str(e),
            "agente": tipo_agente
        }

# 3. ENDPOINTS 
@app.get("/agente/{tipo_agente}/{pregunta}")
def endpoint_agente(tipo_agente: str, pregunta: str):
    return consultar_agente_ia(pregunta, tipo_agente)