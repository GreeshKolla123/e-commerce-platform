from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import User, Product, Order, OrderItem, Cart

router = APIRouter()

@router.post('/login', response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = Session().query(User).filter_by(username=form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/register', response_model=dict)
def register(username: str, email: str, password: str):
    user = Session().query(User).filter_by(username=username).first()
    if user:
        raise HTTPException(status_code=400, detail='Username already exists')
    new_user = User(username=username, email=email, password=pwd_context.hash(password))
    Session().add(new_user)
    Session().commit()
    return {'message': 'User created successfully'}

@router.get('/products', response_model=list)
def get_products(token: str = Depends(oauth2_scheme)):
    products = Session().query(Product).all()
    return products

@router.get('/products/{product_id}', response_model=dict)
def get_product(product_id: int, token: str = Depends(oauth2_scheme)):
    product = Session().query(Product).filter_by(id=product_id).first()
    return product

@router.post('/cart', response_model=dict)
def add_to_cart(product_id: int, quantity: int, token: str = Depends(oauth2_scheme)):
    user = Session().query(User).filter_by(username=token).first()
    cart = Session().query(Cart).filter_by(user_id=user.id, product_id=product_id).first()
    if cart:
        cart.quantity += quantity
    else:
        new_cart = Cart(user_id=user.id, product_id=product_id, quantity=quantity)
        Session().add(new_cart)
    Session().commit()
    return {'message': 'Product added to cart successfully'}

@router.post('/checkout', response_model=dict)
def checkout(token: str = Depends(oauth2_scheme)):
    user = Session().query(User).filter_by(username=token).first()
    cart = Session().query(Cart).filter_by(user_id=user.id).all()
    total = 0
    for item in cart:
        product = Session().query(Product).filter_by(id=item.product_id).first()
        total += product.price * item.quantity
    new_order = Order(user_id=user.id, total=total, status='pending')
    Session().add(new_order)
    Session().commit()
    for item in cart:
        new_order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        Session().add(new_order_item)
    Session().commit()
    return {'message': 'Checkout successful'}
