# Pruebas DevOps - FastAPI + MongoDB

Este proyecto es una API sencilla desarrollada con FastAPI que realiza operaciones básicas relacionadas con listas de enteros y su almacenamiento en una base de datos MongoDB. Es ideal para realizar pruebas y demostraciones relacionadas con el desarrollo y despliegue de aplicaciones.

## Estructura del Proyecto

- **`main.py`**: Contiene el código principal de la API.
- **`Dockerfile`**: Define la imagen Docker para el servicio de FastAPI.
- **`compose.yaml`**: Archivo de configuración de Docker Compose que orquesta los servicios.
- **`client.py`**: Contiene la lógica de conexión a MongoDB.
- **`run.sh`**: Script para gestionar el ciclo de vida del contenedor (detener, eliminar y reconstruir los servicios).

## Requisitos Previos

- Docker
- Docker Compose
- Python 3.12

## Configuración

### Docker

El proyecto está configurado para ejecutarse dentro de contenedores Docker usando Docker Compose. La red Docker `mongodb-net` es utilizada para la comunicación entre los contenedores.

### Variables de Entorno

Las siguientes variables de entorno son utilizadas:

- `MONGODB_HOST`: Nombre del host de MongoDB (definido en `compose.yaml`).
- `MONGODB_PORT`: Puerto en el que se ejecuta MongoDB.

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
docker compose up -d --build
```

Esto levantará los contenedores necesarios (python-api y mongodb), creará las redes y volúmenes necesarios.

### 2. Acceder a la API
La API estará disponible en http://localhost:8000.

### 3. Verificar el Estado del Servicio
Para verificar que la API está corriendo correctamente, puedes acceder al endpoint de healthcheck:
```bash
http://localhost:8000/healthcheck
```

### 4. Volver a construir los Contenedores
Para detener, eliminar y volver a crear los contenedores, volúmenes y la red puede usarse el script llamada:

```bash
./run.sh
```
### Notas Adicionales
- La API es expuesta en el puerto 8000 en el host.
- MongoDB expone el puerto 27017 para permitir conexiones externas.
- El archivo requirements.txt debe contener todas las dependencias de Python necesarias para la aplicación.

# Ejecutar el Proyecto Usando Contenedores y Redes de Docker (Sin Docker Compose)

Este documento detalla los pasos para ejecutar el proyecto utilizando contenedores y redes de Docker, sin depender de `docker-compose`.

## 1. Crear la Red de Docker

Primero, crea una red de Docker para que los contenedores puedan comunicarse entre sí.

```bash
docker network create mongodb-net
```
## 2. Iniciar el Contenedor de MongoDB
Ahora, inicia un contenedor de MongoDB en la red que acabas de crear.

```bash
docker run -d \
  --name mongodb \
  --network mongodb-net \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=mongodb \
  -e MONGO_INITDB_ROOT_PASSWORD=mongodb \
  mvertes/alpine-mongo
```

## 3. Construir la Imagen Docker para la Aplicación FastAPI
A continuación, construye la imagen Docker para tu aplicación FastAPI.

```bash
docker build -t python-api .
```
## 4. Iniciar el Contenedor de la Aplicación FastAPI
Después de construir la imagen, inicia un contenedor basado en ella y conéctalo a la red mongodb-net.

```bash
docker run -d \
  --name python-api \
  --network mongodb-net \
  -p 8000:80 \
  -e MONGODB_HOST=mongodb \
  -e MONGODB_PORT=27017 \
  python-api
  ```

## 6. Gestionar Contenedores y Red
### Parar los Contenedores
Para detener los contenedores, utiliza los siguientes comandos:

```bash
docker stop python-api mongodb
```
### Eliminar los Contenedores
Para eliminar los contenedores después de detenerlos:

```bash
docker rm python-api mongodb
```
### Eliminar la Red
Si deseas eliminar la red de Docker después de haber eliminado los contenedores:

```bash
docker network rm mongodb-net
```