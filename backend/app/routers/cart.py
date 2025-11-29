from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import Cart

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/")
async def create_cart(cart: Cart, db: Session = Depends(get_db)):
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

@router.get("/")
async def read_cart(db: Session = Depends(get_db)):
    return db.query(Cart).all()

@router.put("/{cart_id}")
async def update_cart(cart_id: int, cart: Cart, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db_cart.quantity = cart.quantity
    db.commit()
    db.refresh(db_cart)
    return db_cart

@router.delete("/{cart_id}")
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.delete(db_cart)
    db.commit()
    return {"message": "Cart deleted successfully"}
