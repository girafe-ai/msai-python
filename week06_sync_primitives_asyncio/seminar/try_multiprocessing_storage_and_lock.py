from multiprocessing import Process, freeze_support, Value, Manager, Lock
import ctypes


def task(process_name, test, test_lock):
    test_lock.acquire()
    test.value = test.value + 1  # without lock 2+ Processes can read same value and rewrite each other
    print(process_name, test.value)
    test_lock.release()


if __name__ == '__main__':
    freeze_support()

    # you can create shared Value using Manager
    # manager = Manager()
    # test = manager.Value(ctypes.c_int, 0)

    # or directly
    test = Value(ctypes.c_int, 0)
    lock = Lock()

    processes = []
    for i in range(100):
        # daemon continue to live even if main process finished
        p = Process(target=task, kwargs={'process_name': f'proc {i}', 'test': test, 'test_lock': lock})
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print('proc finished;', '`test` value in main process', test.value)
