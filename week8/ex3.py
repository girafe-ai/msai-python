import os
import threading
import time


def task1():
    print(f"{os.getpid()} is running")
    print(threading.current_thread().name)
    print("Task 1 is running")
    time.sleep(0.5)
    print("Task 1 is complete")


def task2():
    print(f"{os.getpid()} is running")
    print(threading.current_thread().name)
    print("Task 2 is running")
    time.sleep(0.5)
    print("Task 2 is complete")


def main():
    print(f"{os.getpid()} is running")

    t1 = threading.Thread(target=task1)
    t2 = threading.Thread(target=task2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
