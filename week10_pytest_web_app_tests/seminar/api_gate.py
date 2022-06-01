import random

import aiohttp
from aiohttp import web

TEXTS_LIMIT_PER_REQUEST = 10
TEXT_MAX_LENGTH = 1000
TAGGERS_URLS = [
    'http://127.0.0.1:5000/internal/tagging',
    'http://127.0.0.1:5001/internal/tagging',
]
ATTEMPTS = 5


async def handle_tagging(request: web.Request):
    """
    Request:

    POST /tagging HTTP/1.1
    Content-Type: application/json
    Content-Length: 94

    {
        "texts": [
            "text1",
            "text2",
            ...
        ]
    }

    Response:

    HTTP/1.1 200 OK
    Content-Type: application/json
    Content-Length: 94

    {
        "tags": [
            ["text1-tag1", "text1-tag2", ...],
            ["text2-tag1", "text2-tag2", ...],
            ...
        ]
    }
    """
    try:
        request_body = await request.json()
    except Exception:
        return web.json_response(status=400, data={'error': 'Expected JSON body'})

    if (
            not isinstance(request_body, dict) or
            'texts' not in request_body or
            not isinstance(request_body['texts'], list) or
            len(request_body['texts']) > TEXTS_LIMIT_PER_REQUEST or
            any(
                not isinstance(text, str) or len(text) > TEXT_MAX_LENGTH
                for text in request_body['texts']
            )
    ):
        return web.json_response(status=400, data={'error': 'Wrong body format'})

    async with aiohttp.ClientSession() as session:
        for attempt in range(ATTEMPTS):
            tagger_url = random.choice(TAGGERS_URLS)
            try:
                response = await session.post(tagger_url, json=request_body)
            except Exception:
                continue
            if response.status < 500:
                break
        else:
            return web.json_response(status=500, data={'error': 'Internal error'})

        try:
            response_data = await response.json()
        except:
            return web.json_response(status=500, data={'error': 'Internal error'})
        else:
            return web.json_response(status=response.status, data=response_data)


app = web.Application()
app.add_routes([
    web.post('/tagging', handle_tagging)
])

if __name__ == '__main__':
    web.run_app(app)
