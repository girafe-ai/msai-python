import time
from threading import Lock, Thread

# from threading import Semaphore, RLock, Condition, Event, Barrier

counter = 0
# syncronization primitive
lock = Lock()  # mutex


def increment(by):
    global counter
    with lock:
        # lock.acquire()
        local_counter = counter
        local_counter += by
        time.sleep(0.1)
        counter = local_counter
        # lock.release()
    print(f"New counter value: {counter}")


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
