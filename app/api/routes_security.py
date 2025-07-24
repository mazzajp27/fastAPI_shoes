from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import usuario as crud_usuario
from app.security.security import verify_password, create_access_token
from app.models.usuario import Usuarios
from app.schemas.token import Token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token/", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud_usuario.get_usuario_by_email(db, form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": create_access_token({"sub": usuario.email}), "token_type": "Bearer"}


# no minuto 41:57 ele fala sobre aud que fala onde uma pessoa pode mexer no site a partir do token que é gerado
# jwt.io ou debugger.io
# parei no 1:17:10