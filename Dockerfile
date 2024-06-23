# Usa una imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos y el contexto de la aplicación
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación en el contenedor
COPY . .

# Especifica el comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
