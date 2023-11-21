# import asyncio
import time


def f1():
    # send a request to a server
    # wait for the response
    time.sleep(1)
    return "Response from f1"


def f2():
    # send a request to a server
    # wait for the response
    time.sleep(2)
    return "Response from f2"


def main():
    start = time.perf_counter()
    _ = f1()
    _ = f2()
    print("Total time taken: ", time.perf_counter() - start)


if __name__ == "__main__":
    main()
