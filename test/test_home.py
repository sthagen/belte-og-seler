from fastapi.testclient import TestClient

from server import BASE, app

client = TestClient(app)


def test_home():
    response = client.get(f'{BASE}/')
    assert response.status_code == 200
    assert 'Braces' in response.text
