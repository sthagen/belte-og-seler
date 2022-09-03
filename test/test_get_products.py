from fastapi.testclient import TestClient

from server import app

client = TestClient(app)


def test_get_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    products = response.json()
    assert all(["foos" in c for c in products])
    assert all(["bar" in c for c in products])
