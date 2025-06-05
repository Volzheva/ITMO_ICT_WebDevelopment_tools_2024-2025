## Задача 2. Параллельный парсинг веб-страниц с сохранением в базу данных

### Описание задачи
В этой задаче вам необходимо написать программу на Python, которая будет выполнять параллельный парсинг нескольких веб-страниц с использованием подходов `threading`, `multiprocessing` и `async`. Каждая программа должна загружать HTML-страницу по указанному URL, парсить её, сохранять заголовок страницы в базу данных и выводить результат на экран.

### Подробности задания

1. **Использование разных подходов**:
   - Напишите три программы, использующие следующие подходы:
     - **threading** — для параллельной работы с потоками.
     - **multiprocessing** — для параллельной работы с процессами.
     - **async** — для асинхронного выполнения с использованием `asyncio` и `aiohttp`.


2. **Использование базы данных**:
   Для сохранения данных используйте базу данных из лабораторной работы номер 1. Если вам не понятно, какие таблицы и данные нужно заполнять, обратитесь к преподавателю.

3. **Использование модулей**:
   - Для `threading` используйте модуль `threading`.
   - Для `multiprocessing` используйте модуль `multiprocessing`.
   - Для `async` используйте ключевые слова `async/await` и модуль `aiohttp` для асинхронных запросов.


## Примеры
### urls ссылки на сайты с хакатоном
urls =[
    "https://www.хакатоны.рус/tpost/o5y3kpvtj1-architech",
    "https://www.хакатоны.рус/tpost/5fhli252y1-konkurs-avtonomnii-poisk-na-bortu",
    "https://www.хакатоны.рус/tpost/80uis0egp1-go-ctf-2025",
    "https://www.хакатоны.рус/tpost/eculsok1x1-unithack-2025",
    'https://www.хакатоны.рус/tpost/imklbzv241-belie-hakeri',
    'https://www.хакатоны.рус/tpost/1fhvmnaa81-gorod-geroev',
    'https://www.хакатоны.рус/tpost/yd4yk40ta1-forum',

]

### код для парсинга
```python
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from db import SessionLocal, AsyncSessionLocal
from models import Hackathon


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
```

### Время выполнения
async - Completed in 1.459 seconds

threading - Completed in 1.274 seconds

multiprocessing - Completed in  2.445 seconds

Почему быстро:
Асинхронность позволяет не блокировать поток при ожидании ответа от сети (I/O), обрабатывая десятки-запросов "одновременно" в рамках одного потока.

Почему медленнее, чем async:
Потоки тоже ждут ответа от сети, но их переключение и запуск требует больше ресурсов. GIL (Global Interpreter Lock) мешает истинному параллелизму

Почему медленно:
Каждый процесс — это отдельный экземпляр Python-интерпретатора. Создание и синхронизация процессов требует времени и ресурсов. А сетевые запросы (I/O) плохо масштабируются через multiprocessing

