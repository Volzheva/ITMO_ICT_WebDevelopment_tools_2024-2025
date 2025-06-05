from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .database import SessionLocal, AsyncSessionLocal
from .models import Hackathon


html_paths = {
    "title": '#rec488755787 > div > div > div.t-feed__post-popup__container.t-container.t-popup__container.t-popup__container-static > div.t-feed__post-popup__content-wrapper > div:nth-child(3) > div.t-feed__post-popup__title-wrapper > h1',
    'description': '#feed-text > div > section > div > div:nth-child(1)'
}


def extract_text(element, default="N/A"):
    return element.get_text(strip=True) if element else default


def scrape_html(html):
    soup = BeautifulSoup(html, 'lxml')
    title_el = soup.select_one(html_paths["title"])
    desc_el = soup.select_one(html_paths["description"])
    return {
        "title": extract_text(title_el, "No title"),
        "description": extract_text(desc_el, "No description")
    }


def save_sync(html):
    content = scrape_html(html)
    db = SessionLocal()
    try:
        db.add(Hackathon(
            name=content["title"],
            description=content["description"],
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7)
        ))
        db.commit()
    finally:
        db.close()


async def save_async(html):
    content = scrape_html(html)
    async with AsyncSessionLocal() as db:
        db.add(Hackathon(
            name=content["title"],
            description=content["description"],
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7)
        ))
        await db.commit()
