FROM python:3.11-slim

WORKDIR /app

# 1. Copiamos el archivo de dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. COPIAMOS EL CONTENIDO DE BACKEND DIRECTAMENTE
# Esto evita el error de "app.app.main"
COPY backend/ .

# 3. EXPLICITAMOS EL PUERTO
ENV PORT=8080
EXPOSE 8080

# 4. COMANDO DE INICIO ROBUSTO
# Usamos 'python -m' para asegurar que encuentre el paquete 'app'
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]