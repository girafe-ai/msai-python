import asyncio
from time import perf_counter

from common import IO_NAMES, async_io_task, show_elapsed


async def run_tasks() -> None:
    for name in IO_NAMES:
        await async_io_task(name)  # Each task finishes before the next call.


def main() -> float:
    print("10 | Sequential asyncio awaits")
    started = perf_counter()
    asyncio.run(run_tasks())
    return show_elapsed(started)


if __name__ == "__main__":
    main()
