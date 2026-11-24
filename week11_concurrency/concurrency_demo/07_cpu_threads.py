from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from common import CPU_NUMBERS, CPU_WORKERS, is_prime, verdict


def main() -> float:
    print(f"07 | Primality checks with {CPU_WORKERS} threads")
    started = perf_counter()
    with ThreadPoolExecutor(max_workers=CPU_WORKERS) as executor:
        results = list(executor.map(is_prime, CPU_NUMBERS))
    elapsed = perf_counter() - started
    for number, prime in zip(CPU_NUMBERS, results, strict=True):
        print(f"{number} -> {verdict(prime)}")
    print(f"Elapsed: {elapsed:.3f} s")
    return elapsed


if __name__ == "__main__":
    main()
