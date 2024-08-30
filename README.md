# Pruebas DevOps - FastAPI Application

Este proyecto es una aplicación de FastAPI diseñada para pruebas relacionadas con DevOps.

## 1. Ejecución Directa con Python

### Instalación de Dependencias

1. Clona el repositorio y navega al directorio del proyecto:

    ```bash
    git clone https://github.com/JuanPabloMoralesG/practicas_devops.git
    cd practicas_devops
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

### Ejecución de la Aplicación

4. Ejecuta la aplicación FastAPI:

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

5. La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

## 2. Ejecución usando Docker

### Construcción de la Imagen Docker

1. Construye la imagen Docker:

    ```bash
    docker build -t python-api .
    ```

### Ejecución del Contenedor

2. Ejecuta la aplicación en un contenedor:

    ```bash
    docker run -p 8000:80 python-api
    ```

3. La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

## 3. Ejecución usando Docker Compose

### Ejecución con `docker-compose`

1. Ejecuta la aplicación usando `docker-compose`:

    ```bash
    docker-compose up --build
    ```

2. La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

### Detener la Aplicación

3. Para detener la aplicación, usa:

    ```bash
    docker-compose down
    ```

