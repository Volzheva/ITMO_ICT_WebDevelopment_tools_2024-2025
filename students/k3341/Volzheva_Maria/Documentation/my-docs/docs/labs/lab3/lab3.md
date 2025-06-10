# Лабораторная работа 3. Упаковка FastAPI приложения в Docker, Работа с источниками данных и Очереди

## Цель работы
Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь

Dockerfile FastAPI-приложение:
```
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

Dockerfile парсере:
```
FROM python:3.9

WORKDIR /parser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
```
Файл celery_worker.py:
``` python
from celery import Celery
import asyncio
import httpx

from hackathon.urls import urls
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@celery_app.task(name="parse_url")
def parse_url_tasks(url: str):
    return asyncio.run(_parse_url(url))


@celery_app.task(name="parse_all_urls")
def parse_all_urls():
    return asyncio.run(_parse_all_urls())


async def _parse_url(url: str):
    try:
        async with httpx.AsyncClient() as client:
            html_response = await client.get(url)
            parser_response = await client.post(
                "http://parser:9000/parse",
                json={"html": html_response.text}
            )
            return parser_response.json()
    except Exception as e:
        return {"error": str(e), "url": url}


async def _parse_all_urls():
    results = []
    for url in urls:
        result = await _parse_url(url)
        results.append(result)
    return results
```
Файл docker-compose.yml:
```
version: "3.8"

services:
  db:
    image: postgres:14
    container_name: hackathon_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: hackathon_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: redis
    restart: always
    ports:
      - "6379:6379"

  hackathon:
    build:
      context: ./hackathon
      dockerfile: Dockerfile
    container_name: hackathon_app
    depends_on:
      - db
      - redis
    env_file:
      - ./hackathon/.env
    ports:
      - "8000:8000"
    volumes:
      - ./hackathon:/app
    command: ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

  parser:
    build:
      context: ./parser
      dockerfile: Dockerfile
    container_name: parser_app
    depends_on:
      - db
    env_file:
      - ./parser/task2/.env
    ports:
      - "9000:9000"
    volumes:
      - ./parser:/parser
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

  celery_worker:
    build:
      context: ./hackathon
      dockerfile: Dockerfile
    container_name: celery_worker
    depends_on:
      - redis
      - hackathon
    command: ["celery", "-A", "celery_worker", "worker", "--loglevel=info"]
    volumes:
      - ./hackathon:/app
    environment:
      - CELERY_BROKER=redis://redis:6379/0
      - CELERY_BACKEND=redis://redis:6379/0

volumes:
  postgres_data:
```

## Сборка приложения:
```
docker-compose up --build
```


