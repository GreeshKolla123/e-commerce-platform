from fastapi import APIRouter
from app.models import Cart
from app.database import Session

router = APIRouter(
    prefix='/api/cart',
    tags=['cart'],
)

@router.post('/')
async def add_to_cart(product_id: int, quantity: int):
    cart = Cart(user_id=1, product_id=product_id, quantity=quantity)
    Session.add(cart)
    Session.commit()
    return {'cart': [{'product_id': c.product_id, 'quantity': c.quantity} for c in Session.query(Cart).all()]}

@router.get('/')
async def get_cart():
    cart = Session.query(Cart).all()
    return [{'product_id': c.product_id, 'quantity': c.quantity} for c in cart]
