# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias
COPY ../Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

# Copiar el código del dashboard al directorio de trabajo
COPY ../ .

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la API
# Se usa --host 0.0.0.0 para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
