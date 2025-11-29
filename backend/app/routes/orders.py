from fastapi import APIRouter
from app.models import Order
from app.database import Session

router = APIRouter(
    prefix='/api/orders',
    tags=['orders'],
)

@router.post('/')
async def checkout(cart: list):
    order = Order(user_id=1, total=sum([c['price'] * c['quantity'] for c in cart]))
    Session.add(order)
    Session.commit()
    return {'order_id': order.id}

@router.get('/')
async def get_orders():
    orders = Session.query(Order).all()
    return [{'id': o.id, 'user_id': o.user_id, 'total': o.total} for o in orders]
