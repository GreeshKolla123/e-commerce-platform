from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import Order

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/")
async def create_order(order: Order, db: Session = Depends(get_db)):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/")
async def read_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.get("/{order_id}")
async def read_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.id == order_id).first()
