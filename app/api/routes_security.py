from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm,  OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import user as crud_user
from app.security.security import verify_password, create_access_token, verify_token, get_current_user
from app.models.user import User
from app.schemas.token import Token
from datetime import timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token/", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para login e obtenção de tokens de acesso
    """
    user = crud_user.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": create_access_token({"sub": user.email, "tipo": user.type}), "token_type": "Bearer"}


# no minuto 41:57 ele fala sobre aud que fala onde uma pessoa pode mexer no site a partir do token que é gerado
# jwt.io ou debugger.io
# parei no 1:17:10