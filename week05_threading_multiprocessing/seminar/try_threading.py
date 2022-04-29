from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep

# one way to receive results from threads - to put them into storage
# second way - to use inheritance, create storage for 1 result and overload join method to return that result
# (details - https://stackoverflow.com/a/6894023)
result_storage = {}


def task(result_key, *args, **kwargs):
    print(f'task started: {args}, {kwargs}')

    # imitate CPU bound task ~10 sec
    # for _ in range(10 ** 8):
    #     i = 1

    # imitate I/O bound task
    sleep(5)

    print(f'task finishing: {args}, {kwargs}')

    task_result = kwargs.get('name', 'no name') + ' result'
    result_storage[result_key] = task_result
    return task_result


threads = []
for i in range(10):
    t = Thread(target=task, args=(i,), kwargs={'name': f'task {i}'})
    t.start()
    threads.append([t, i])
    print('t.start()')

print('break')

for t, i in threads:
    t.join()
    print(f'{i} t.join(). result: {result_storage[i]}')


pool = ThreadPoolExecutor(max_workers=5)
results = []
for i in range(10):
    result = pool.submit(task, i, name=f'task {i}')
    results.append(result)
    print(type(result), result)

print('all tasks submitted')

for r in results:
    print(r.result())
