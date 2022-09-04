from unittest.mock import Mock

from fastapi.testclient import TestClient

from model import Product, ProductInput, User
from router.products import add_product
from server import app

client = TestClient(app)


def test_add_product():
    data = {'description': 'yes', 'product': 'oh', 'family': 'no'}
    response = client.post('/api/products/', json=data, headers={'Authorization': 'Bearer rotor'})
    assert response.status_code == 200
    product = response.json()
    assert product['description'] == data['description']
    assert product['product'] == data['product']
    assert product['family'] == data['family']


def test_add_product_with_mock_session():
    mock_session = Mock()
    input = ProductInput(family='no', product='yes', description='lengthy')
    user = User(username='rotor')
    result = add_product(product_input=input, session=mock_session, user=user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert isinstance(result, Product)
    assert result.family == 'no'
    assert result.product == 'yes'
