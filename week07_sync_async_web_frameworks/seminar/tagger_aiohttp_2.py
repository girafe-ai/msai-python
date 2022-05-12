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


def tagging_job(texts):
    tags = [set() for _ in texts]  # [{text1-tag1, text1-tag2, ...}, ...]
    for tagger in taggers:
        result = tagger.get_tags(texts)
        # merge tags of same text from different taggers
        for text_tags_set, text_tags in zip(tags, result):
            text_tags_set |= set(text_tags)

    tags = [list(text_tags_set) for text_tags_set in tags]
    return {
        'tags': tags
    }


async def handle_tagging(request: web.Request):
    texts = (await request.json())['texts']
    loop = request.app.loop
    result = await loop.run_in_executor(executor, tagging_job, texts)
    return web.json_response(data={'tags': result})


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.post('/internal/tagging', handle_tagging)
    ])
    web.run_app(app, port=8001)
