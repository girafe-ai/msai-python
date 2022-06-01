from unittest.mock import patch, Mock

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


async def test_hello(gate_client):
    with patch('aiohttp.ClientSession') as ClientSessionMock:
        ClientSessionMock.return_value = MockSession()
        response = await gate_client.post("/tagging", json={'texts': ['text']})

    assert response.status == 200
    data = await response.json()
    assert data == FAKE_DATA
