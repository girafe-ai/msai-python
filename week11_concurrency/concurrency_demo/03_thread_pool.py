from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from common import IO_NAMES, io_task, show_elapsed

WORKERS = 4


def main() -> float:
    print(f"03 | Waiting with a thread pool of {WORKERS} workers")
    started = perf_counter()
    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="Worker") as executor:
        results = list(executor.map(io_task, IO_NAMES))
    print(f"Results in input order: {results}")
    return show_elapsed(started)


if __name__ == "__main__":
    main()
