# Usamos la imagen oficial de Python como base
FROM python:3.12-alpine

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /opt/python-api

# Copiamos los archivos necesarios al contenedor
COPY main.py client.py requirements.txt ./

# Instalamos las dependencias dentro de un entorno virtual
RUN python -m venv /opt/python-api/venv \
    && /opt/python-api/venv/bin/pip install --upgrade pip \
    && /opt/python-api/venv/bin/pip install -r requirements.txt

# Exponemos el puerto 80 para acceder a la API
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["/opt/python-api/venv/bin/python", "main.py"]
