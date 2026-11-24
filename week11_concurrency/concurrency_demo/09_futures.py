from concurrent.futures import Future, ThreadPoolExecutor
from time import perf_counter

from common import io_task, show_elapsed

JOBS = (("A", 1.0), ("B", 0.4))


def main() -> float:
    print("09 | Futures from submit()")
    started = perf_counter()
    with ThreadPoolExecutor(max_workers=len(JOBS), thread_name_prefix="Worker") as executor:
        futures: list[Future[str]] = [executor.submit(io_task, name, delay) for name, delay in JOBS]
        print(f"submit() returned Future objects. Done now: {[future.done() for future in futures]}")
        print("Calling result() in submission order. It waits if the Future is still pending.")
        results = [future.result() for future in futures]
        print(f"Results: {results}. Done now: {[future.done() for future in futures]}")
    return show_elapsed(started)


if __name__ == "__main__":
    main()
