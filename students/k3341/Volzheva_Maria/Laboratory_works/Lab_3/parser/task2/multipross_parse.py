import time
import requests
import logging
from multiprocessing import Process
from parser import save_sync
from database import init_db
from urls import urls


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def process_urls(batch):
    for link in batch:
        try:
            logging.info(f"Fetching: {link}")
            resp = requests.get(link, timeout=10)
            resp.raise_for_status()
            save_sync(resp.text)
            logging.info(f"Saved data from: {link}")
        except requests.RequestException as err:
            logging.error(f"Failed to process {link}: {err}")

def run_parallel():
    init_db()
    workers = 3
    step = (len(urls) + workers - 1) // workers
    segments = [urls[i:i+step] for i in range(0, len(urls), step)]
    jobs = []

    for part in segments:
        p = Process(target=process_urls, args=(part,))
        p.start()
        jobs.append(p)
        logging.info(f"Spawned process {p.pid}")

    for job in jobs:
        job.join()
        logging.info(f"Process {job.pid} completed")

if __name__ == "__main__":
    t0 = time.perf_counter()
    logging.info("Begin parsing")
    run_parallel()
    t1 = time.perf_counter()
    logging.info(f"Completed in {t1 - t0:.3f} seconds")

#Completed in 1.687 seconds