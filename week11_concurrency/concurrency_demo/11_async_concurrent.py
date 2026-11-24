import asyncio
from time import perf_counter

from common import IO_NAMES, async_io_task, show_elapsed


async def run_tasks() -> None:
    first, *remaining = IO_NAMES
    coroutine = async_io_task(first)
    task = asyncio.create_task(coroutine)
    print(f"create_task() scheduled {first}. Done now: {task.done()}")
    results = await asyncio.gather(task, *(async_io_task(name) for name in remaining))
    print(f"Results in input order: {results}")


def main() -> float:
    print("11 | Concurrent asyncio tasks")
    started = perf_counter()
    asyncio.run(run_tasks())
    return show_elapsed(started)


if __name__ == "__main__":
    main()
