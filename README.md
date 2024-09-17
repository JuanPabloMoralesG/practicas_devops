# Pruebas DevOps - FastAPI + MongoDB

Este proyecto es una API sencilla desarrollada con FastAPI que realiza operaciones básicas relacionadas con listas de enteros y su almacenamiento en una base de datos MongoDB. Es ideal para realizar pruebas y demostraciones relacionadas con el desarrollo y despliegue de aplicaciones.

## Estructura del Proyecto

- **`main.py`**: Contiene el código principal de la API.
- **`Dockerfile`**: Define la imagen Docker para el servicio de FastAPI.
- **`docker-compose.yaml`**: Archivo de configuración de Docker Compose que orquesta los servicios.
- **`client.py`**: Contiene la lógica de conexión a MongoDB.
- **`run.sh`**: Script para gestionar el ciclo de vida del contenedor (detener, eliminar y reconstruir los servicios).

## Configuración

### Docker

El proyecto está configurado para ejecutarse dentro de contenedores Docker usando Docker Compose. La red Docker `mongodb-net` es utilizada para la comunicación entre los contenedores.

### Variables de Entorno

Las siguientes variables de entorno son utilizadas:

- `MONGODB_HOST`: Nombre del host de MongoDB.
- `MONGODB_PORT`: Puerto en el que se ejecuta MongoDB.
- `TZ`: Zona horaria que se le asociara al contenedor de la aplicacion.

## Endpoints de la API

### 1. `/lista-ordenada`

- **Descripción**: Ordena una lista de enteros proporcionada en formato JSON.
- **Método**: `GET`
- **Parámetro**: `lista-no-ordenada` (str) - Cadena JSON que representa una lista de enteros.
- **Respuesta**: 
  - **200 OK**: JSON con la lista ordenada y la hora actual.
  - **400 Bad Request**: Si la entrada no es válida, retorna un mensaje de error.

### 2. `/healthcheck`

- **Descripción**: Verifica el estado del servicio.
- **Método**: `GET`
- **Respuesta**:
  - **200 OK**: Texto plano con el contenido "OK".

### 3. `/guardar-lista-no-ordenada`

- **Descripción**: Guarda una lista no ordenada en MongoDB con un UUID y la fecha actual.
- **Método**: `GET`
- **Parámetro**: `lista-no-ordenada` (str) - Cadena JSON que representa una lista de enteros.
- **Respuesta**:
  - **200 OK**: JSON con un mensaje que indica si la lista fue guardada exitosamente o si hubo un error.

## Instrucciones de Uso

### 1. Ejecutar el Proyecto con Docker Compose
```bash
docker compose up -d --build [nombre del servicio]
```

Esto levantará los contenedores necesarios (python-api y mongodb), creará las redes y volúmenes necesarios.

### 2. Acceder a la API
La API estará disponible en http://localhost:8000.

### 3. Verificar el Estado del Servicio
Para verificar que la API está corriendo correctamente, puedes acceder al endpoint de healthcheck:
```bash
http://localhost:8000/healthcheck
```

# Ejecutar el Proyecto Usando Contenedores, Redes de Docker y Volumenes (Sin Docker Compose)

Este documento detalla los pasos para ejecutar el proyecto utilizando contenedores y redes de Docker, sin depender de `docker-compose`.

## 1. Crear la Red de Docker

Primero, crea una red de Docker para que los contenedores puedan comunicarse entre sí.

```
docker network create --driver bridge mongodb-net
```

## 2. Crear el volumen mongo_data
Docker necesita un volumen para persistir los datos de MongoDB. Crea el volumen manualmente con:
```
docker volume create --name mongo_data
```

## 3. Iniciar el Contenedor de MongoDB
Ahora, inicia un contenedor de MongoDB en la red que acabas de crear.

```
docker run -d \
  --name mongodb \
  --hostname mongodb \
  --network mongodb-net \
  -v mongo_data:/data/db \
  -p 27017:27017 \
  --restart always \
  mvertes/alpine-mongo
```

## 4. Construir la Imagen Docker para la Aplicación FastAPI
Primero, debes navegar al directorio app/, que contiene el código fuente y el archivo Dockerfile. Luego, ejecuta el siguiente comando para construir la imagen:

```
docker build -t python-api ./app/
```
## 5. Ejecutar el contenedor de la API Python
Una vez que la imagen está construida, puedes ejecutar el contenedor de la API Python. Asegúrate de que las variables de entorno necesarias (MONGODB_HOST, MONGODB_PORT, TZ) estén configuradas.
```
docker run -d \
  --name python-api \
  --hostname python-api \
  --network mongodb-net \
  -e MONGODB_HOST=${MONGODB_HOST} \
  -e MONGODB_PORT=${MONGODB_PORT} \
  -e TZ=${TZ} \
  -v $(pwd)/volumes/logs/info.log:/opt/python-api/logs/info.log \
  -v $(pwd)/app/main.py:/opt/python-api/main.py \
  -v $(pwd)/app/client.py:/opt/python-api/client.py \
  -v $(pwd)/app/requirements.txt:/opt/python-api/requirements.txt \
  -p 8000:80 \
  --restart always \
  python-api

```

## 6. Gestionar Contenedores y Red
### Verificar la ejecución de los contenedores
Puedes verificar que los contenedores estén corriendo usando el siguiente comando:
```
docker ps
```
### Ver los logs de los contenedores:
Para ver los logs de un contenedor, puedes usar:
```
docker logs python-api
docker logs -f python-api
```

### Parar los Contenedores
Para detener los contenedores, utiliza los siguientes comandos:
```
docker stop python-api mongodb
```

### Eliminar los Contenedores
Para eliminar los contenedores después de detenerlos:
```
docker rm python-api mongodb
```
### Eliminar los volumenes
Para eliminar los volumenes después de detener los contenedores:
```
docker volume rm mongo_data
```
### Eliminar la Red
Si deseas eliminar la red de Docker después de haber eliminado los contenedores:
```
docker network rm mongodb-net
```