import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

class IntentSchema(BaseModel):
    dominio: str = Field(description="Dominio detectado: FAMILIA, PROFESIONAL, ESTUDIOS o GENERAL")
    razonamiento: str = Field(description="Breve explicación de por qué se eligió este dominio")

class ClassifierAgent:
    def __init__(self):
        # Usamos Gemini para la clasificación inteligente
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    async def classify(self, query: str, history: str = "") -> IntentSchema:
        prompt = f"""
        Actúa como un clasificador de intenciones experto para un sistema RAG.
        Contexto del historial: {history}
        Pregunta del usuario: {query}
        
        Clasifica en uno de estos dominios:
        - FAMILIA: Preguntas sobre hijos (Sebastián, Pablo, Leandro), esposa (Tatiana) o vida personal.
        - PROFESIONAL: Preguntas sobre carrera, experiencia en Ayesa, CV o LinkedIn.
        - ESTUDIOS: Preguntas sobre el Máster de IA o cursos en Big Data Academy.
        - GENERAL: Saludos o temas no relacionados.
        """
        return await self.llm.with_structured_output(IntentSchema).ainvoke(prompt)