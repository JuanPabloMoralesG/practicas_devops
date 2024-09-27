FROM python:3.12-slim

WORKDIR /opt/api-monitor

COPY . .

RUN python -m venv /opt/api-monitor/venv \
    && /opt/api-monitor/venv/bin/pip install --upgrade pip \
    && /opt/api-monitor/venv/bin/pip install -r requirements.txt

EXPOSE 80

CMD ["/opt/api-monitor/venv/bin/python", "monitoreo_script.py"]