from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, DecodeError
from app.models.usuario import Usuarios
from app.database import SessionLocal
from app.schemas.token import TokenData

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_coontext = PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_coontext.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_coontext.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    # data é o email do usuario
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(SessionLocal), token: str = Depends(oauth2_scheme)):   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    user = db.scalar(select(Usuarios).where(Usuarios.email == email))
    if not user:
        raise credentials_exception
    return user 
   