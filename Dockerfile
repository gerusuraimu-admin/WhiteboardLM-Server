FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./utils /app/utils
COPY ./main.py /app/main.py

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "8080", "--log-level", "warning"]