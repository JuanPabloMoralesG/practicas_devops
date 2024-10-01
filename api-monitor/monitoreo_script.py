import os
import time
import logging
import requests

# Configuración del host y puerto del contenedor objetivo
TARGET_CONTAINER_HOST = os.getenv('TARGET_CONTAINER_HOST', 'localhost')
TARGET_CONTAINER_PORT = os.getenv('TARGET_CONTAINER_PORT', '80')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL',10))
HEALTHCHECK_ENDPOINT = f'http://{TARGET_CONTAINER_HOST}:{TARGET_CONTAINER_PORT}/healthcheck'

# Configuración del logging
logging.basicConfig(
    filename='api-monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def check_health():
    try:
        response = requests.get(HEALTHCHECK_ENDPOINT, timeout=5)
        if response.status_code == 200 and response.text.strip() == 'OK':
            logging.info(f' Se hizo la solicitud al endpoint 
                         http://api-container:8000/healthcheck y devolvió {response.text}')
            print(f' Se hizo la solicitud al endpoint 
                  http://api-container:8000/healthcheck y devolvió {response.text}')
        else:
            logging.error(f'Se hizo la solicitud al endpoint 
                         http://api-container:8000/healthcheck y devolvió error:
                          Código de estado: {response.status_code}, Respuesta: {response.text}')
            print(f'Se hizo la solicitud al endpoint 
                  http://api-container:8000/healthcheck y devolvió error:
                  Código de estado: {response.status_code}, Respuesta: {response.text}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Fallo la solicitud al endpoint 
                      http://api-container:8000/healthcheck y devolvió error:
                      Respuesta: {str(e)}')
        print(f'Fallo la solicitud al endpoint 
              http://api-container:8000/healthcheck y devolvió error:
              Respuesta: {str(e)}')

if __name__ == "__main__":
    while True:
        check_health()
        time.sleep(CHECK_INTERVAL)
