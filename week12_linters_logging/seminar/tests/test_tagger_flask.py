def test_request_example(flask_client):
    response = flask_client.post('/internal/tagging', json={'texts': ['text']})
    assert response.status_code == 200
    assert response.json == {'tags': [['comp.windows.x']]}
