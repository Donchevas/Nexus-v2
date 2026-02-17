from collections import deque

class MemoryManager:
    def __init__(self, limit: int = 5):
        """
        Mantiene un historial de las últimas interacciones por usuario.
        limit: Número de intercambios (pregunta/respuesta) a recordar.
        """
        self.limit = limit
        # Diccionario para manejar múltiples usuarios si fuera necesario
        self.user_histories = {}

    def add_interaction(self, user_id: str, query: str, response: str):
        """Añade una nueva interacción al historial del usuario."""
        if user_id not in self.user_histories:
            self.user_histories[user_id] = deque(maxlen=self.limit)
        
        self.user_histories[user_id].append({
            "query": query,
            "response": response
        })

    def get_context_string(self, user_id: str) -> str:
        """Retorna el historial formateado como string para el ClassifierAgent."""
        if user_id not in self.user_histories or not self.user_histories[user_id]:
            return "No hay historial previo."
        
        context = ""
        for interaction in self.user_histories[user_id]:
            context += f"Usuario: {interaction['query']}\nNexus: {interaction['response']}\n---\n"
        return context

    def clear_memory(self, user_id: str):
        """Limpia el historial del usuario."""
        if user_id in self.user_histories:
            self.user_histories[user_id].clear()