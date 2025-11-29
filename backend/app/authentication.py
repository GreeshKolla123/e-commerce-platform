from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

class TokenData(BaseModel):
    username: str | None = None

def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')
    return encoded_jwt

async def get_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail='Could not validate credentials')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = Session.query(User).filter_by(username=token_data.username).first()
    if not user:
        raise credentials_exception
    return user

async def authenticate_user(username: str, password: str):
    user = Session.query(User).filter_by(username=username).first()
    if not user:
        return False
    if not user.password == password:
        return False
    return user
