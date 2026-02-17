import httpx
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importamos tus agentes y configuración
from app.agents.classifier import ClassifierAgent
from app.agents.memory import MemoryManager
from app.core.config import settings

# Configuración de logs para monitoreo profesional
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nexus v2 Orchestrator - Clean Architecture")

# 1. BYPASS DE SEGURIDAD (CORS) - Libre de Firebase
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de la Inteligencia de Agentes
classifier = ClassifierAgent()
memory = MemoryManager(limit=5) # Mantiene las últimas 5 interacciones en memoria

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def handle_chat(chat_req: ChatRequest):
    try:
        query = chat_req.message
        # Usamos tu ID de identidad para la persistencia de la memoria
        user_id = settings.USER_ID_MAESTRO 

        # --- FASE 1: INTUICIÓN ALINEADA (Agentes) ---
        # Recuperamos el contexto previo para que Nexus no "olvide" de quién habla
        history_context = memory.get_context_string(user_id)
        
        # El Classifier determina si la pregunta es FAMILIA, PROFESIONAL o ESTUDIOS
        intent_result = await classifier.classify(query, history=history_context)
        dominio_detectado = intent_result.dominio
        
        logger.info(f"Nexus v2 - Query: {query} | Dominio: {dominio_detectado}")

        # --- FASE 2: COMUNICACIÓN CON EL MOTOR RAG ---
        async with httpx.AsyncClient() as client:
            # Enviamos el payload limpio al motor en Cloud Run
            payload = {
                "user_id": user_id,
                "query": query, 
                "dominio": dominio_detectado 
            }
            
            # Usamos la URL configurada en core/config.py
            response = await client.post(
                settings.MOTOR_RAG_URL, 
                json=payload, 
                timeout=30.0
            )
            
            if response.status_code != 200:
                return {"response": f"Error del Motor RAG: {response.status_code}", "dominio": dominio_detectado}

            res_json = response.json()
            response_text = res_json.get("response", "Nexus no pudo recuperar información.")

        # --- FASE 3: PERSISTENCIA Y RETORNO ---
        # Guardamos la interacción para que la charla fluya con armonía
        memory.add_interaction(user_id, query, response_text)
        
        return {
            "dominio": dominio_detectado,
            "response": response_text
        }

    except Exception as e:
        logger.error(f"Falla crítica en Orquestador: {str(e)}")
        return {"response": f"Error técnico en Nexus v2: {str(e)}"}

@app.get("/health")
async def health_check():
    return {"status": "online", "version": "v2.0.0-minimal"}