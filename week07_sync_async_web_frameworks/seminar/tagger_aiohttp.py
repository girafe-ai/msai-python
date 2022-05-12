import asyncio
# from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

from aiohttp import web

from taggers import MostFrequentWordsTagger, FindSpecialWordsTagger, SGDClassifierTagger

taggers = [
    MostFrequentWordsTagger(),
    FindSpecialWordsTagger(),
    SGDClassifierTagger()
]
# executor = ThreadPoolExecutor(max_workers=4)  # threaded variant
executor = ProcessPoolExecutor(max_workers=4)  # processed variant


async def handle_tagging(request: web.Request):
    texts = (await request.json())['texts']

    # create awaitable futures that waits response from executors
    # (we use separate workers for taggers to run them simultaneously)
    futures = []
    loop = request.app.loop
    for tagger in taggers:
        future = loop.run_in_executor(executor, tagger.get_tags, texts)
        futures.append(future)

    # wait all taggers finished
    results = await asyncio.gather(*futures)

    # merge tags of same text from different taggers
    tags = [set() for _ in texts]  # [{text1-tag1, text1-tag2}, ...]
    for result in results:
        for text_tags_set, text_tags in zip(tags, result):
            text_tags_set |= set(text_tags)

    tags = [list(text_tags_set) for text_tags_set in tags]
    return web.json_response(data={'tags': tags})


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.post('/internal/tagging', handle_tagging)
    ])
    web.run_app(app, port=8001)
