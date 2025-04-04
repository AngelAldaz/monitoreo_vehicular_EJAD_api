# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos primero para aprovechar el caching de Docker
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Expone el puerto en el que corre FastAPI (normalmente 8000)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app", "--port", "8000"]