from threading import Lock, Thread
from time import perf_counter, sleep

from common import show_elapsed

WORKERS = 100
INCREMENTS = 100
DELAY = 0.00001


def main() -> float:
    print("05 | Protect a shared counter with a lock")
    counter = 0
    lock = Lock()

    def increment(name: str) -> None:
        nonlocal counter
        for attempt in range(INCREMENTS):
            with lock:        
                value = counter
                sleep(DELAY)
                counter = value + 1


    started = perf_counter()
    threads = [Thread(target=increment, args=(f"Worker {i + 1}",)) for i in range(WORKERS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Expected: {WORKERS * INCREMENTS}\nActual:   {counter}\nLost:     {WORKERS * INCREMENTS - counter}")
    return show_elapsed(started)


if __name__ == "__main__":
    main()
