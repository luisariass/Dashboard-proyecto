# config.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi
import logging
import asyncio

# Cargar variables del .env
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")  # Base principal del proyecto

logging.basicConfig(level=logging.INFO)

# Variables globales de BD
db = None
db_google = None

try:
    # Conexión asíncrona con Motor (cliente async)
    client = AsyncIOMotorClient(
        MONGODB_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )

    # Motor no se conecta hasta que hagas la primera operación async,
    # así que no usamos client.server_info() directamente (bloquearía el loop)
    db = client[MONGODB_DATABASE]
    db_google = client["Googlemaps_Scraping"]

    print(" Conexión asíncrona a MongoDB inicializada")
    print("   Base principal:", db.name)
    print("   Base Google Maps:", db_google.name)

except Exception as e:
    logging.error(" Error de conexión a MongoDB: %s", e)
    db = None
    db_google = None
