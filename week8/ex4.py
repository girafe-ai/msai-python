import time
from threading import Thread

counter = 0


def increment(by):
    global counter
    local_counter = counter
    local_counter += by
    time.sleep(0.1)
    counter = local_counter
    print(f"New counter value: {counter}")


# t1 -> local_counter = 10 -> sleep -> t2 -> local_counter = 50 -> sleep
# 1. t1 is first -> counter = 10 -> t2 wakes -> counter = 50
# 2. t2 is first -> counter = 50 -> t1 wakes -> counter = 10
def main():
    # race condition
    t1 = Thread(target=increment, args=(10,))
    t2 = Thread(target=increment, args=(50,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Counter value: {counter}")


if __name__ == "__main__":
    main()
