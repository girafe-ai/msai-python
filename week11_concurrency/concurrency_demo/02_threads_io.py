from threading import Thread, current_thread
from time import perf_counter

from common import IO_NAMES, io_task, show_elapsed


def main() -> float:
    print("02 | Waiting with explicit threads")
    started = perf_counter()
    print(f"{current_thread().name}: start four workers")
    workers = [Thread(target=io_task, args=(name,), name=f"Worker-{name}") for name in IO_NAMES]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    print(f"{current_thread().name}: all workers joined")
    return show_elapsed(started)


if __name__ == "__main__":
    main()
