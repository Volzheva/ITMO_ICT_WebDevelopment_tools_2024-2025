from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from hackathon.celery_worker import parse_url_tasks, parse_all_urls, celery_app
from urllib.parse import urlparse, unquote
import idna
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def normalize_url(url: str) -> str:
    """Конвертирует кириллические домены в Punycode"""
    decoded_url = unquote(url)
    parsed = urlparse(decoded_url)

    if any(ord(char) > 127 for char in parsed.netloc):
        domain = idna.encode(parsed.netloc).decode('ascii')
        return decoded_url.replace(parsed.netloc, domain)
    return decoded_url


@router.post("/parse-all")
def parse_all():
    try:
        logger.info("Запуск парсинга всех URL")
        task = parse_all_urls.delay()
        return {"task_id": task.id}
    except Exception as e:
        logger.error(f"Ошибка в parse_all: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/parse-url")
def parse_url(url: str):
    try:
        logger.info(f"Получен URL для парсинга: {url}")
        normalized_url = normalize_url(url)
        logger.info(f"Нормализованный URL: {normalized_url}")

        task = parse_url_tasks.delay(normalized_url)
        logger.info(f"Создана задача Celery: {task.id}")

        return {"task_id": task.id}
    except Exception as e:
        logger.error(f"Ошибка при обработке URL {url}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task-status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task_result.status,
    }

    if task_result.ready():
        if task_result.failed():
            response.update({
                "status": "failed",
                "error": str(task_result.result),
                "traceback": task_result.traceback
            })
        else:
            response["result"] = task_result.result

    return response