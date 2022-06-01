import pytest

from api_gate import app as aiohttp_app
from tagger_flask import app as flask_app


@pytest.fixture()
def flask_client():
    return flask_app.test_client()


@pytest.fixture()
async def gate_client(aiohttp_client):
    return await aiohttp_client(aiohttp_app)
