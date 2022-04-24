from unittest.mock import Mock
from fastapi.testclient import TestClient

from server import app
from router.products import add_product
from model import ProductInput, User, Product

client = TestClient(app)


def test_add_product():
    response = client.post("/api/products/",
                           json={
                               "foos": 7,
                               "bar": "xxl"
                           }, headers={'Authorization': 'Bearer rotor'}
                           )
    assert response.status_code == 200
    product = response.json()
    assert product['foos'] == 7
    assert product['bar'] == 'xxl'


def test_add_product_with_mock_session():
    mock_session = Mock()
    input = ProductInput(foos=2, bar="xl")
    user = User(username="rotor")
    result = add_product(product_input=input, session=mock_session, user=user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert isinstance(result, Product)
    assert result.foos == 2
    assert result.bar == "xl"
