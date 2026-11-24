from threading import Thread
from time import perf_counter, sleep

from common import show_elapsed

WORKERS = 100
INCREMENTS = 100
DELAY = 0.00001


def main() -> float:
    print("04 | Race condition on a shared counter")
    print(f"{WORKERS} workers attempt {INCREMENTS} increments each.")
    print("On the first increment, every worker reads before any worker writes.")
    counter = 0

    def worker() -> None:
        nonlocal counter
        for attempt in range(INCREMENTS):
            value = counter
            sleep(DELAY)
            counter = value + 1

    started = perf_counter()
    threads = [Thread(target=worker) for _ in range(WORKERS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    expected = WORKERS * INCREMENTS
    print(f"Expected: {expected}\nActual:   {counter}\nLost:     {expected - counter}")
    return show_elapsed(started)


if __name__ == "__main__":
    main()
