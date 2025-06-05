import time
import requests
from threading import Thread
from parser import save_sync
from database import init_db
from urls import urls


def handle_batch(batch):
    for link in batch:
        try:
            resp = requests.get(link, timeout=10)
            resp.raise_for_status()
            save_sync(resp.text)
        except requests.RequestException as e:
            print(f"Error: {link} — {e}")


def run_threads():
    init_db()
    workers = 3
    step = (len(urls) + workers - 1) // workers
    segments = [urls[i:i + step] for i in range(0, len(urls), step)]

    threads = [Thread(target=handle_batch, args=(seg,)) for seg in segments]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    t0 = time.perf_counter()
    run_threads()
    t1 = time.perf_counter()
    print(f"Completed in {t1 - t0:.3f} seconds")

#Completed in 1.357 seconds