import asyncio
from math import isqrt
from threading import current_thread
from time import perf_counter, sleep

IO_NAMES = ("A", "B", "C", "D")
IO_DELAY = 1.0
CPU_NUMBERS = (
    100_000_000_000_031,
    100_000_000_000_067,
    100_000_000_000_097,
    10_000_019 ** 2,  # A composite whose first divisor is near the end of the search.
    100_000_000_000_099,
    10_000_000_000_037,
    10_000_000_000_051,
    10_000_000_000_099,
    4_000_037 ** 2,
    5_000_011 ** 2,
)
CPU_WORKERS = 4


def io_task(name: str, delay: float = IO_DELAY) -> str:
    worker = current_thread().name
    print(f"{worker}: start {name}", flush=True)
    # Sleep simulates a task that spends most of its time waiting for I/O.
    sleep(delay)
    print(f"{worker}: end   {name}", flush=True)
    return name


async def async_io_task(name: str, delay: float = IO_DELAY) -> str:
    print(f"start {name}", flush=True)
    await asyncio.sleep(delay)
    print(f"end   {name}", flush=True)
    return name


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    for divisor in range(3, isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False
    return True


def verdict(prime: bool) -> str:
    return "prime" if prime else "composite"


def show_elapsed(started: float) -> float:
    elapsed = perf_counter() - started
    print(f"Elapsed: {elapsed:.3f} s")
    return elapsed
