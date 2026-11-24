from time import perf_counter

from common import CPU_NUMBERS, is_prime, verdict


def main() -> float:
    print("06 | Sequential primality checks")
    started = perf_counter()
    results = [is_prime(number) for number in CPU_NUMBERS]
    elapsed = perf_counter() - started
    for number, prime in zip(CPU_NUMBERS, results, strict=True):
        print(f"{number} -> {verdict(prime)}")
    print(f"Elapsed: {elapsed:.3f} s")
    return elapsed


if __name__ == "__main__":
    main()
