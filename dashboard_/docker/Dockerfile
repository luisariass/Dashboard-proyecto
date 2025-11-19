# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias
COPY ../Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

# Copiar el código del dashboard al directorio de trabajo
COPY ../ .

# Exponer el puerto 8501
EXPOSE 8501

# Comando para ejecutar el dashboard de Streamlit
CMD ["streamlit", "run", "app.py"]
