from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.security.security import get_password_hash
from datetime import datetime
from fastapi import HTTPException
from app.models.buyer import Buyer
from app.models.seller import Seller


def get_user(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user: UserCreate):

    db_user = User(
        full_name=user.full_name,
        cpf = user.cpf,
        email=user.email,
        birthdate=user.birthdate,
        gender=user.gender,
        password=get_password_hash(user.password),
        is_active=user.is_active if hasattr(user, 'is_active') else True,
        is_superuser=user.is_superuser,
        is_buyer=user.is_buyer,
        is_seller=user.is_seller,
        created_at=datetime.utcnow()
    )
    
    db.add(db_user)
    db.flush()  # Obtém o user_id sem fazer commit
    
    # 5. Se is_buyer = true, criar Buyer automaticamente
    if user.is_buyer:
        db_buyer = Buyer(
            user_id=db_user.user_id,
            preferences= None  
        )
        db.add(db_buyer)
    
    # 6. Se is_seller = true, criar Seller automaticamente
    if user.is_seller:
        db_seller = Seller(
            user_id=db_user.user_id,
            store_name= None,
            cnpj= None,
            description= None  
        )
        db.add(db_seller)
    
    # 7. Commit de tudo
    db.commit()
    db.refresh(db_user)
    
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def alter_status_user(db: Session, user_id: int):
    """Deleta user (soft delete - marca como inativo)"""
    db_user = db.query(User).filter(User.user_id == user_id).first()
    
    if db_user is None:
        return None
    
    # Soft delete - marca o User como inativo
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id: int):
    db_user = db.query(User).filter(User.user_id == id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()