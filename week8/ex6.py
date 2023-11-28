import threading
import time
from concurrent.futures import ThreadPoolExecutor


def is_prime(x: int) -> bool:
    if x < 2:
        return False
    for i in range(2, x):
        if x % i == 0:
            return False
    return True


# GIL -> Global Interpreter Lock -> only one thread can run CPU instruction at a time
# GIL Cpython
def main():
    # option1: sequential
    # start = time.perf_counter()
    # for i in range(100000):
    #     is_prime(i)
    # end = time.perf_counter()
    # print(f"Time taken: {end - start}")

    # option2: multithreading
    # start = time.perf_counter()
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     _ = executor.map(is_prime, range(100000))
    # end = time.perf_counter()
    # print(f"Time taken: {end - start}")

    # option3: threading
    start = time.perf_counter()
    threads = []
    for i in range(100000):
        t = threading.Thread(target=is_prime, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end = time.perf_counter()
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    main()
