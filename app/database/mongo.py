import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Se lee la URI y el nombre de la base de datos desde las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# Se crea el cliente de conexión a MongoDB
client = MongoClient(MONGO_URI)

# Se selecciona la base de datos
db = client[MONGO_DB]

# Se selecciona la colección de sesiones
sessions_collection = db[MONGO_COLLECTION]