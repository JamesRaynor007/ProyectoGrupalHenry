# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt . 
COPY scripts/ ./scripts/
COPY proyecto-resto-score-f02454a3aee3.json /app/proyecto-resto-score-f02454a3aee3.json


# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto: Ejecutar el script principal
CMD ["python", "/app/scripts/main.py"]
