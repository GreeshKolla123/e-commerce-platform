from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models import User
from app.database import Session
from app.config import settings
from app.authentication import authenticate_user, create_access_token

router = APIRouter(
    prefix='/api/users',
    tags=['users'],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

@router.post('/register')
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User(username=form_data.username, email=form_data.username, password=form_data.password)
    Session.add(user)
    Session.commit()
    return {'token': create_access_token(user.id)}

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    return {'token': create_access_token(user.id)}
