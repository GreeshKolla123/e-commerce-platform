from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os

# Create the database engine
engine = create_engine('postgresql://user:password@localhost/dbname')

# Create the session maker
Session = sessionmaker(bind=engine)

# Create the base class for the models
Base = declarative_base()

# Create the models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    orders = relationship('Order', backref='user')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    order_items = relationship('OrderItem', backref='product')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total = Column(Float)
    status = Column(String)
    order_items = relationship('OrderItem', backref='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

# Create the tables
Base.metadata.create_all(engine)

# Create the FastAPI app
app = FastAPI()

# Create the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Create the password context
pwd_context = CryptContext(schemes=['bcrypt'], default='bcrypt')

# Create the secret key
SECRET_KEY = 'secret_key'

# Create the algorithm
ALGORITHM = 'HS256'

# Create the access token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create the token endpoint
@app.post('/login', response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = Session().query(User).filter_by(username=form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

# Create the register endpoint
@app.post('/register', response_model=dict)
async def register(username: str, email: str, password: str):
    user = Session().query(User).filter_by(username=username).first()
    if user:
        raise HTTPException(status_code=400, detail='Username already exists')
    new_user = User(username=username, email=email, password=pwd_context.hash(password))
    Session().add(new_user)
    Session().commit()
    return {'message': 'User created successfully'}

# Create the products endpoint
@app.get('/products', response_model=list)
async def get_products(token: str = Depends(oauth2_scheme)):
    products = Session().query(Product).all()
    return products

# Create the product endpoint
@app.get('/products/{product_id}', response_model=dict)
async def get_product(product_id: int, token: str = Depends(oauth2_scheme)):
    product = Session().query(Product).filter_by(id=product_id).first()
    return product

# Create the cart endpoint
@app.post('/cart', response_model=dict)
async def add_to_cart(product_id: int, quantity: int, token: str = Depends(oauth2_scheme)):
    user = Session().query(User).filter_by(username=token).first()
    cart = Session().query(Cart).filter_by(user_id=user.id, product_id=product_id).first()
    if cart:
        cart.quantity += quantity
    else:
        new_cart = Cart(user_id=user.id, product_id=product_id, quantity=quantity)
        Session().add(new_cart)
    Session().commit()
    return {'message': 'Product added to cart successfully'}

# Create the checkout endpoint
@app.post('/checkout', response_model=dict)
async def checkout(token: str = Depends(oauth2_scheme)):
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
