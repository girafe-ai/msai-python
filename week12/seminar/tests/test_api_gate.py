from unittest.mock import patch, Mock

import pytest
from models import User, manager

FAKE_DATA = {
    "tags": [
        ["text1-tag1", "text1-tag2"],
        ["text2-tag1", "text2-tag2"],
    ]
}


class MockSession:
    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    async def post(self, *args, **kwargs):
        print('Somebody called mocked post with', args, kwargs)

        async def _fake_json():
            return FAKE_DATA

        response = Mock()
        response.status = 200
        response.json = _fake_json
        return response


async def test_ok(gate_client):
    api_key = 'e721y87e30'
    await manager.create(User, name='test-user', api_key=api_key)

    with patch('aiohttp.ClientSession') as ClientSessionMock:
        ClientSessionMock.return_value = MockSession()
        response = await gate_client.post("/tagging?api_key=e721y87e30", json={'texts': ['text']})

    assert response.status == 200
    data = await response.json()
    assert data == FAKE_DATA


@pytest.mark.parametrize(
    'api_key_url_part',
    ['', '?api_key=']  # , '?api_key=123'
)
async def test_bad_api_key(gate_client, api_key_url_part):
    with patch('aiohttp.ClientSession') as ClientSessionMock:
        ClientSessionMock.return_value = MockSession()
        response = await gate_client.post(
            "/tagging" + api_key_url_part,
            json={'texts': ['text']}
        )

    assert response.status == 403
