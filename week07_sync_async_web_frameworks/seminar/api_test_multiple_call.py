import asyncio
import aiohttp


async def test(task_num):
    print(task_num, 'sent')
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            'http://0.0.0.0:8080/tagging',
            json={'texts': ['God is love', 'OpenGL on the GPU is fast']}
        )
        print(task_num, response.status, await response.text())


loop = asyncio.get_event_loop()

coros = [test(i) for i in range(100)]
c_all = asyncio.gather(*coros)

result = loop.run_until_complete(c_all)
print(len(result))
