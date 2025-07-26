from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, DecodeError
from app.models.usuario import Usuarios

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


