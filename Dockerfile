FROM python:3.11-alpine

WORKDIR /opt/python-api

COPY . .

RUN python -m venv /opt/python-api/venv \
    && /opt/python-api/venv/bin/pip install --upgrade pip \
    && /opt/python-api/venv/bin/pip install -r requirements.txt

EXPOSE 80

CMD ["/opt/python-api/venv/bin/python", "main.py"]
