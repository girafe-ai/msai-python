import asyncio
import time


async def factorial(n):
    f = 1
    for i in range(1, n):
        f *= i
    return f


async def main():
    start = time.perf_counter()
    tasks = []
    for i in range(4000):
        tasks.append(asyncio.create_task(factorial(i)))
    await asyncio.gather(*tasks)
    print(f"Time taken: {time.perf_counter() - start} seconds")


if __name__ == "__main__":
    asyncio.run(main())
