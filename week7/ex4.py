import asyncio
import time


# coroutine function
async def f1():
    # send a request to a server
    # wait for the response
    print("f1 started")

    # time.sleep(1)
    await asyncio.sleep(1)

    return "Response from f1"


async def f2():
    # send a request to a server
    # wait for the response
    print("f2 started")

    # time.sleep(2)
    await asyncio.sleep(2)

    return "Response from f2"


async def main():
    start = time.perf_counter()
    tasks = []
    tasks.append(asyncio.create_task(f1()))
    tasks.append(asyncio.create_task(f2()))

    # for task in asyncio.as_completed(tasks):
    #     await task
    await asyncio.gather(*tasks)

    print("Total time taken: ", time.perf_counter() - start)


if __name__ == "__main__":
    # print(type(main()))
    asyncio.run(main())
