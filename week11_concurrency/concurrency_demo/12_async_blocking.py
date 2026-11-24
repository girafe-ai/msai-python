import asyncio
from time import perf_counter, sleep

from common import show_elapsed

WAIT = 1.0
TICK_INTERVAL = 0.25
TICKS = 6


async def heartbeat(started: float) -> None:
    for tick in range(1, TICKS + 1):
        print(f"{perf_counter() - started:5.2f} s | heartbeat {tick}", flush=True)
        if tick < TICKS:
            await asyncio.sleep(TICK_INTERVAL)


async def blocking_wait() -> None:
    print("        blocking wait starts", flush=True)
    sleep(WAIT)
    print("        blocking wait ends", flush=True)


async def cooperative_wait() -> None:
    print("        async wait starts", flush=True)
    await asyncio.sleep(WAIT)
    print("        async wait ends", flush=True)


async def compare() -> None:
    for label, wait in (("Blocking sleep", blocking_wait), ("Cooperative sleep", cooperative_wait)):
        print(f"\n{label}")
        await asyncio.gather(heartbeat(perf_counter()), wait())


def main() -> float:
    print("12 | What happens when the event loop is blocked?")
    started = perf_counter()
    asyncio.run(compare())
    return show_elapsed(started)


if __name__ == "__main__":
    main()
