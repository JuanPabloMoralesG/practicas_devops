import datetime
import json
import logging
import uuid
import uvicorn

from client import get_mongo
from fastapi import FastAPI, status, Query
from fastapi.responses import JSONResponse, PlainTextResponse


app = FastAPI(
    title='Pruebas DevOps',
    version='1.0.0',
    description='Una API sencilla para pruebas relacionadas con DevOps'
)
logging.basicConfig(
    filename="/opt/python-api/logs/info.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("fastapi_logger")



@app.get(path='/lista-ordenada',
         description="End point para ordenar una lista de enteros.",
         response_description="Un JSON con la fecha actual y la lista ordenada.",
         status_code=status.HTTP_200_OK
         )
def lista_ordenada(lista_no_ordenada: str =
                   Query(..., alias="lista-no-ordenada")) \
        -> JSONResponse:
    """
    Ordena una lista de números enteros proporcionada en formato str.

    :param lista_no_ordenada: Una cadena de texto que representa una lista de
    números enteros en formato JSON. Ejemplo: `"[3, 1, 2]"`.
    :return: - **200 OK**: Retorna un JSON con la hora actual del sistema y la
    lista ordenada.
    - **400 Bad Request**: Si la entrada no es una lista de enteros válida,
        se devuelve un mensaje de error.
    """
    try:
        lista_no_ordenada = lista_no_ordenada.strip('[]').split(',')
        lista_no_ordenada = [int(i) for i in lista_no_ordenada]
        lista = sorted(lista_no_ordenada)
    except:
        logger.error("No se ingreso una lista de enteros en formato de texto")
        return JSONResponse("Error al convertir la entrada en una lista",
                            status_code=status.HTTP_400_BAD_REQUEST)
    data = {
        "hora_sistema": str(datetime.datetime.now()),
        "lista_ordenada": lista
    }
    return JSONResponse(data, status_code=status.HTTP_200_OK)


@app.get(path='/healthcheck',
         description="End point para verificar el estado del servicio.",
         response_description="Texto plano con un 'OK'.",
         status_code=status.HTTP_200_OK
         )
def lista_ordenada() -> PlainTextResponse:
    """
    Verifica que el servicio esté funcionando correctamente.

    :return:
    - **200 OK**: Retorna un texto plano con el contenido "OK".
    """
    return PlainTextResponse(content="OK",
                             status_code=status.HTTP_200_OK)


@app.get(path='/guardar-lista-no-ordenada',
         description="Guarda una lista no ordenada en la base de datos con un UUID y la fecha actual.",
         response_description="Un mensaje indicando si la lista fue guardada exitosamente o si hubo un error.",
         status_code=status.HTTP_200_OK
         )
def guardar_lista_no_ordenada(lista_no_ordenada:str =
                              Query(..., alias='lista-no-ordenada')) \
-> JSONResponse:
    """
    Guarda una lista no ordenada en una colección de MongoDB.

    :param lista_no_ordenada: Una cadena JSON que representa una lista
    de enteros no ordenada.
    :return: **JSONResponse**: Un JSON que contiene un mensaje indicando
    si la lista fue guardada correctamente y el UUID asignado, o un mensaje
    de error si la operación falló.
    """
    sta = status.HTTP_200_OK
    collection = get_mongo()
    id = uuid.uuid4()
    lista: list[int] = json.loads(lista_no_ordenada)
    dato_nuevo = {
        "_id": str(id),
        "fecha":str(datetime.datetime.now()),
        "lista":lista
    }
    text = ""
    try:
        collection.insert_one(dato_nuevo)
        text = f"La lista ordenada fue guardada con el id: {id}"
    except Exception as e:
        text = "Error guardanto la lista"
        logger.error(e)
        sta = status.HTTP_500_INTERNAL_SERVER_ERROR

    data = { "msg" : text }
    return JSONResponse(content=data,status_code=sta)


if __name__ == '__main__':
    """
    Punto de entrada principal para ejecutar la aplicación con Uvicorn.
    """
    uvicorn.run(app="main:app", host="0.0.0.0", port=80, reload=True)
