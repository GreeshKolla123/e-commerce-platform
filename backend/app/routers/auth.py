from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from app.config import Settings
from app.database import get_db
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_user(db, username: str):
    user_dict = db.query(User).filter(User.username == username).first()
    if not user_dict:
        return False
    return user_dict

@router.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(get_db(), form_data.username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = pwd_context.hash(form_data.password)
    user = User(username=form_data.username, email=form_data.username, password=hashed_password)
    get_db().add(user)
    get_db().commit()
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(get_db(), form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = jwt.encode(
        claims={"sub": user.username},
        key=Settings().SECRET_KEY,
        algorithm=Settings().ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}
