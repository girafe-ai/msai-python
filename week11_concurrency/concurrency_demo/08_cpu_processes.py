from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from os import getpid
from time import perf_counter

from common import CPU_NUMBERS, CPU_WORKERS, is_prime, verdict

TINY_NUMBERS = (97, 101, 103, 105)


def check_in_process(number: int) -> tuple[bool, int]:
    return is_prime(number), getpid()


def main() -> float:
    print(f"08 | Primality checks with {CPU_WORKERS} processes")
    print(f"Parent PID: {getpid()}")
    started = perf_counter()
    # Spawn starts fresh interpreters, including on Windows.
    with ProcessPoolExecutor(max_workers=CPU_WORKERS, mp_context=get_context("spawn")) as executor:
        results = list(executor.map(check_in_process, CPU_NUMBERS))
    elapsed = perf_counter() - started
    for number, (prime, pid) in zip(CPU_NUMBERS, results, strict=True):
        print(f"{number} -> {verdict(prime)} (worker PID {pid})")

    tiny_start = perf_counter()
    tiny_results = [is_prime(number) for number in TINY_NUMBERS]
    sequential = perf_counter() - tiny_start
    tiny_start = perf_counter()
    with ProcessPoolExecutor(max_workers=CPU_WORKERS, mp_context=get_context("spawn")) as executor:
        process_results = list(executor.map(is_prime, TINY_NUMBERS))
    parallel = perf_counter() - tiny_start
    assert process_results == tiny_results
    print(f"Tiny workload, same {len(TINY_NUMBERS)} checks in each run:")
    print(f"Sequential: {sequential:.6f} s | New process pool: {parallel:.3f} s")
    print(f"Elapsed (main workload): {elapsed:.3f} s")
    return elapsed


if __name__ == "__main__":
    main()
