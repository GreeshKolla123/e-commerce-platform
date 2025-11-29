from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post('/api/users/register', json={'username': 'test', 'email': 'test@example.com', 'password': 'test'})
    assert response.status_code == 200

def test_login():
    response = client.post('/api/users/login', json={'username': 'test', 'password': 'test'})
    assert response.status_code == 200

def test_get_products():
    response = client.get('/api/products/')
    assert response.status_code == 200

def test_get_product():
    response = client.get('/api/products/1')
    assert response.status_code == 200

def test_add_to_cart():
    response = client.post('/api/cart/', json={'product_id': 1, 'quantity': 1})
    assert response.status_code == 200

def test_get_cart():
    response = client.get('/api/cart/')
    assert response.status_code == 200

def test_checkout():
    response = client.post('/api/orders/', json=[{'product_id': 1, 'quantity': 1, 'price': 10.99}])
    assert response.status_code == 200

def test_get_orders():
    response = client.get('/api/orders/')
    assert response.status_code == 200
