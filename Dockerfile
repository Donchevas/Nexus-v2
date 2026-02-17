FROM python:3.11-slim

WORKDIR /app

# Copiamos desde la raíz del repo al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la carpeta backend al contenedor
COPY backend/ .

EXPOSE 8080

# Al copiar 'backend/', el archivo main queda en /app/app/main.py
# Por eso el comando es app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]