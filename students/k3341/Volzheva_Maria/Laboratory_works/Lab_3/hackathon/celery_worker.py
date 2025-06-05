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
