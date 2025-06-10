import asyncio
import time
import aiohttp
import logging

from parser import save_async
from database import async_init_db
from urls import urls

logging.basicConfig(level=logging.INFO)

async def get_html(session, link):
    try:
        async with session.get(link, timeout=10, ssl=False) as resp:
            return await resp.text()
    except Exception as err:
        logging.error(f"Failed to fetch {link}: {err}")
        return None

async def handle_url(session, link):
    html = await get_html(session, link)
    if html:
        logging.debug(f"Fetched content from {link}:\n{html[:1000]}")
        await save_async(html)
    else:
        logging.warning(f"Empty response from {link}")

async def process_batch(batch):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(handle_url(session, url) for url in batch))

async def run_all():
    await async_init_db()

    total = len(urls)
    parts = 3
    step = (total + parts - 1) // parts
    split_urls = [urls[i:i+step] for i in range(0, total, step)]

    await asyncio.gather(*(process_batch(part) for part in split_urls))

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(run_all())
    end = time.perf_counter()
    print(f"Completed in {end - start:.3f} seconds")

#Completed in 0.575 seconds