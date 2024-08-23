import uvicorn
import datetime
import json

from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI(
    title='Pruebas DevOps',
    version='1.0.0'
)


@app.get(path='/lista-ordenada',
         )
def lista_ordenada(lista_no_ordenada: str) -> JSONResponse:
    lista: List[int] = json.loads(lista_no_ordenada)
    data = {
        "hora_sistema": str(datetime.datetime.now()),
        "lista_ordenada": list(sorted(lista))
    }
    return JSONResponse(data, status_code=200)


@app.get(path='/healthcheck',
         )
def lista_ordenada() -> PlainTextResponse:
    return PlainTextResponse(content="OK", status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
