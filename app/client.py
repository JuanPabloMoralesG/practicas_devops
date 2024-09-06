import logging
import os

from pymongo.mongo_client import MongoClient

logger = logging.getLogger('uvicorn.error')
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT = os.getenv("MONGODB_PORT")

url = f'mongodb://{MONGODB_HOST}:mongodb@mongodb:{MONGODB_PORT}/'

def get_mongo():
    """
    Establece una conexión a MongoDB y devuelve una colección específica.

    :returns collection: La colección `listas_no_ordenadas` dentro de la 
    base de datos `python_app`.
    """
    client = MongoClient(url)
    try:
        client.admin.command('ping')
    except Exception as e:
        logger.error(e)
    
    db = client['python_app']
    collection = db['listas_no_ordenadas']
    logger.info("Conectado a la bd")
    return collection
