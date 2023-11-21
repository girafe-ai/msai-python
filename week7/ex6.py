import time


# CPU bound function
# Does not involve any I/O
def factorial(n):
    f = 1
    for i in range(1, n):
        f *= i
    return f


def main():
    start = time.perf_counter()
    for i in range(4000):
        _ = factorial(i)
    print(f"Time taken: {time.perf_counter() - start} seconds")


if __name__ == "__main__":
    main()
