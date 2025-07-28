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
from typing import Optional

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

pwd_context = PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    # data é o email do usuario
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Removendo verificação de tipo por enquanto
        # if payload.get("type") != token_type:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Tipo de token inválido"
        #     )
        return payload
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token, "access")
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except HTTPException:
        raise credentials_exception
    
    user = db.scalar(select(Usuarios).where(Usuarios.email == email))
    if not user:
        raise credentials_exception
    
    # Verificar se o usuário está ativo
    if user.status != "ativo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user 
   
   
def get_current_cliente(db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_user)):
    """Verifica se o usuário autenticado é um cliente"""
    if current_user.tipo != "clientes":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas clientes podem acessar este recurso."
        )
    return current_user

def get_current_admin(db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_user)):
    """Verifica se o usuário autenticado é um administrador"""
    if current_user.tipo != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem acessar este recurso."
        )
    return current_user

def get_current_vendedor(db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_user)):
    """Verifica se o usuário autenticado é um vendedor"""
    if current_user.tipo != "vendedor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas vendedores podem acessar este recurso."
        )
    return current_user

