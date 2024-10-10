import os
import time
import logging
import requests

TARGET_CONTAINER_HOST = os.getenv('TARGET_CONTAINER_HOST', 'localhost')
"""str: Nombre o dirección IP del host del contenedor objetivo. 
Por defecto, 'localhost'."""

TARGET_CONTAINER_PORT = os.getenv('TARGET_CONTAINER_PORT', '80')
"""str: Puerto del contenedor objetivo. Por defecto, '80'."""

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 10))
"""int: Intervalo de tiempo (en segundos) entre cada verificación de estado. Por defecto, 10 segundos."""

HEALTHCHECK_ENDPOINT = f'http://{TARGET_CONTAINER_HOST}:{TARGET_CONTAINER_PORT}/healthcheck'
"""str: URL completa del endpoint de verificación de salud."""

# Configuración del logging
logging.basicConfig(
    filename='logs/api-monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
"""Configura el sistema de logging para escribir los registros en el archivo 'logs/api-monitor.log'."""


def check_health():
    """Verifica el estado de salud del contenedor objetivo.

    Realiza una solicitud HTTP GET al endpoint de verificación de salud 
    del contenedor. Si la respuesta es 'OK' con código de estado 200, se 
    registra como éxito; de lo contrario, se registra como error. Los 
    errores de conexión también son capturados y registrados.

    Excepciones capturadas:
        requests.exceptions.RequestException: Error en la solicitud HTTP.
    """
    try:
        response = requests.get(HEALTHCHECK_ENDPOINT, timeout=5)
        if response.status_code == 200 and response.text.strip() == 'OK':
            logging.info(f'Se hizo la solicitud al endpoint {HEALTHCHECK_ENDPOINT} y devolvió {response.text}')
            print(f'Se hizo la solicitud al endpoint {HEALTHCHECK_ENDPOINT} y devolvió {response.text}')
        else:
            logging.error(f'Se hizo la solicitud al endpoint {HEALTHCHECK_ENDPOINT} y devolvió error: Código de estado: {response.status_code}, Respuesta: {response.text}')
            print(f'Se hizo la solicitud al endpoint {HEALTHCHECK_ENDPOINT} y devolvió error: Código de estado: {response.status_code}, Respuesta: {response.text}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Fallo la solicitud al endpoint {HEALTHCHECK_ENDPOINT} y devolvió error: Respuesta: {str(e)}')
        print(f'Fallo la solicitud al endpoint {HEALTHCHECK_ENDPOINT} y devolvió error: Respuesta: {str(e)}')


if __name__ == "__main__":
    while True:
        check_health()
        time.sleep(CHECK_INTERVAL)
