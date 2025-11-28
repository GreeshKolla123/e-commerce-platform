from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post('/register', json={'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'})
    assert response.status_code == 200
    assert response.json()['message'] == 'User created successfully'

def test_login_user():
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_get_products():
    response = client.get('/products', headers={'Authorization': 'Bearer <access_token>'})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product():
    response = client.get('/products/1', headers={'Authorization': 'Bearer <access_token>'})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_add_to_cart():
    response = client.post('/cart', json={'product_id': 1, 'quantity': 2}, headers={'Authorization': 'Bearer <access_token>'})
    assert response.status_code == 200
    assert response.json()['message'] == 'Product added to cart successfully'

def test_checkout():
    response = client.post('/checkout', headers={'Authorization': 'Bearer <access_token>'})
    assert response.status_code == 200
    assert response.json()['message'] == 'Checkout successful'
