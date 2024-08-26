import uvicorn
import datetime
import json
import logging

from typing import List
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI(
    title='Pruebas DevOps',
    version='1.0.0'
)
logger = logging.getLogger('uvicorn.error')

@app.get(path='/lista-ordenada',
         description="end pint para ordenar una lista",
         response_description="un json con la fecha actual y la lista ordenada",
         status_code=status.HTTP_200_OK
         )
def lista_ordenada(lista_no_ordenada: str) -> JSONResponse:
    try:    
        lista: List[int] = json.loads(lista_no_ordenada)
    except:
        logger.error("No se ingreso una lista de enteros en formato de texto")
        return JSONResponse("Error al convertir la entrada en una lista", 
                            status_code=status.HTTP_400_BAD_REQUEST)
    data = {
        "hora_sistema": str(datetime.datetime.now()),
        "lista_ordenada": sorted(lista)
    }
    return JSONResponse(data, status_code=status.HTTP_200_OK)


@app.get(path='/healthcheck',
         description="end point para checkear el servicio",
         response_description="texto plano con un OK",
         status_code=status.HTTP_200_OK
         )
def lista_ordenada() -> PlainTextResponse:
    return PlainTextResponse(content="OK", 
                             status_code=status.HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)