FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN pip install --no-cache-dir fastapi[all] firebase-admin google-cloud-pubsub

COPY ./app /app