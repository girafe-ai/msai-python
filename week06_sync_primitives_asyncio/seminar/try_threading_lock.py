import time
from threading import Thread, Lock


class MyList:
    def __init__(self):
        self.storage = []
        self.storage_size = 0
        self.lock = Lock()

    def append(self, element):
        self.lock.acquire()
        current_size = self.storage_size  # without lock 2+ threads can read same storage_size
        time.sleep(0.00001)
        self.storage.append(element)
        self.storage_size = current_size + 1  # and rewrite each other's results
        self.lock.release()


my_list = MyList()


class CheckThread(Thread):
    def run(self):
        for i in range(1000):
            my_list.append(i)


threads = [CheckThread() for i in range(100)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(my_list.storage_size)
