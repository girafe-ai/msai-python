from multiprocessing import Process, freeze_support
from time import sleep

test = 1


def task(*args, **kwargs):
    print(f'task started: {args}, {kwargs}')

    # doesn't affect main process
    global test
    test = 2

    # imitate CPU bound task ~10 sec
    # for _ in range(10 ** 8):
    #     i = 1

    # imitate I/O bound task
    sleep(10)

    print(f'task finishing: {args}, {kwargs}')

    return kwargs.get('name', 'no name') + ' result'


if __name__ == '__main__':
    freeze_support()

    processes = []
    for i in range(10):
        # daemon continue to live even if main process finished
        p = Process(target=task, kwargs={'name': f'proc {i}'}, daemon=True)
        p.start()
        processes.append(p)
        print('proc started')

    for p in processes:
        p.join()
        print('proc finished;', '`test` value in main process', test)
