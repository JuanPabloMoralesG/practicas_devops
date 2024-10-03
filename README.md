# Pruebas DevOps - FastAPI + MongoDB

Este proyecto es una API sencilla desarrollada con FastAPI que realiza operaciones básicas relacionadas con listas de enteros y su almacenamiento en una base de datos MongoDB. Es ideal para realizar pruebas y demostraciones relacionadas con el desarrollo y despliegue de aplicaciones.

## Configuración

### Docker

El proyecto está configurado para ejecutarse dentro de contenedores Docker usando Docker Compose. La red Docker `mongodb-net` es utilizada para la comunicación entre los contenedores.

### Variables de Entorno

Las siguientes variables de entorno son utilizadas:

- `CHECK_INTERVAL`: Intervalo en segundos entre cada intento de verificación del estado del api.
- `TARGET_CONTAINER_HOST`: Nombre del host del contenedor objetivo al que la aplicación se conectará.
- `TARGET_CONTAINER_PORT`: Puerto del contenedor objetivo al que la aplicación intentará conectarse.
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
```
docker-compose --profile [nombre servicio] up 
```

Usar el profile 'back' levantará los contenedores necesarios, creará las redes y volúmenes actualmente desarrollados

### 2. Acceder a la API
La API estará disponible en http://localhost:8000.

### 3. Verificar el Estado del Servicio
Para verificar que la API está corriendo correctamente, puedes acceder al endpoint de healthcheck:
```
http://localhost:8000/healthcheck
```
### 4. Detener los servicios
Para detener y elimindar la informacion creada por el docker compose se usan los comandos:
```
docker compose --profile back down
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

## 6. Construir la Imagen Docker para la Aplicación de Monitoreo
Primero, debes navegar al directorio donde se encuentra el archivo Dockerfile. Luego, ejecuta el siguiente comando para construir la imagen:

```
docker build -t api-monitor .
```
Este comando construirá una imagen llamada api-monitor basada en el archivo Dockerfile del directorio actual.

## 7. Ejecutar el Contenedor de la Aplicación de Monitoreo
Una vez que la imagen esté construida, puedes ejecutar el contenedor de la aplicación. Asegúrate de que las variables de entorno necesarias (MONGODB_HOST, MONGODB_PORT, TZ) estén configuradas.

```
docker run -d \
  --name api-monitor \
  --hostname api-monitor \
  --network <nombre-red> \
  -e MONGODB_HOST=${MONGODB_HOST} \
  -e MONGODB_PORT=${MONGODB_PORT} \
  -e TZ=${TZ} \
  -v $(pwd)/logs:/opt/api-monitor/logs \
  -v $(pwd)/monitoreo_script.py:/opt/api-monitor/monitoreo_script.py \
  -v $(pwd)/requirements.txt:/opt/api-monitor/requirements.txt \
  -p 8000:80 \
  --restart always \
  api-monitor
  ```

## 8. Gestionar Contenedores y Red
### Verificar la ejecución de los contenedores
Puedes verificar que los contenedores estén corriendo usando el siguiente comando:
```
docker ps
```
### Ver los logs de los contenedores:
Para ver los logs de un contenedor, puedes usar:
```
docker logs [nombre contenedor]
docker logs -f [nombre contenedor]
```

### Parar los Contenedores
Para detener los contenedores, utiliza los siguientes comandos:
```
docker stop [nombre contenedor]
```

### Eliminar los Contenedores
Para eliminar los contenedores después de detenerlos:
```
docker rm [nombre contenedor]
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
