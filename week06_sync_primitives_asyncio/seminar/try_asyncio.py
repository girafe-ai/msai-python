import asyncio
# import time

import aiohttp
# import requests


async def imitate_http_request():
    print('Starting request...')
    await asyncio.sleep(1)  # release control to main loop for a second
    # time.sleep(1)  # don't do that - this is synchronous operation
    return 'response'


async def do_http_request():
    print('Starting request...')

    # that will stops code execution until response received
    # response = requests.get('http://example.com/')

    # => need to use packages that support asyncio
    # they will release control for the moment of waiting
    async with aiohttp.ClientSession() as session:
        response = await session.get('http://example.com/')
        return response


def parse_response(response):
    # not possible to run coroutines in synchronous code
    # await asyncio.sleep(1)

    print(f'response status_code={response.status}')
    if response:
        return response
    else:
        return 'error'


async def test(task_num, *args, **kwargs):
    response = await do_http_request()
    print('task #', task_num, ' - response received')
    return parse_response(response)


loop = asyncio.get_event_loop()

coros = [test(i) for i in range(100)]
c_all = asyncio.gather(*coros)

result = loop.run_until_complete(c_all)
print(len(result))
