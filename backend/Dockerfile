# backend/Dockerfile

FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get install \
    'postgresql' \
    'postgresql-contrib' \
    'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

COPY . .

EXPOSE 8080

CMD gunicorn --timeout=60 --bind 0.0.0.0:8080 main:app -k uvicorn.workers.UvicornWorker

#CMD ["python", "main.py"]
