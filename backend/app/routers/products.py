from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import Product

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/")
async def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}")
async def read_product(product_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.id == product_id).first()
