# app/crud/buyer.py
from sqlalchemy.orm import Session, joinedload
from app.models.buyer import Buyer
from app.models.user import User
from app.schemas.buyer import BuyerBase, BuyerCreate, BuyerCreateWithUser, BuyerUpdate, BuyerDisplay
from app.security.security import get_password_hash
from sqlalchemy import text
from fastapi import Depends, HTTPException
from app.security.security import get_current_user


def get_buyers(db: Session):
    """Retorna todos os buyers com User carregado"""
    return db.query(Buyer).options(joinedload(Buyer.user)).all()


def get_buyer(db: Session, buyer_id: int):
    """Busca buyer por buyer_id com User carregado"""
    return db.query(Buyer).options(joinedload(Buyer.user)).filter(Buyer.buyer_id == buyer_id).first()


def create_buyer(db: Session, buyer_data: BuyerCreateWithUser):
    # 1. Verificar se email/telefone já existem
    if db.query(User).filter(User.email == buyer_data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if db.query(User).filter(User.phone_number == buyer_data.phone_number).first():
        raise HTTPException(status_code=400, detail="Telefone já cadastrado")
    
    # 2. Criar User com is_buyer=True
    db_user = User(
        full_name=buyer_data.full_name,
        cpf=buyer_data.cpf,
        email=buyer_data.email,
        birthdate=buyer_data.birthdate,
        gender=buyer_data.gender,
        password=get_password_hash(buyer_data.password),
        is_active=True,
        is_superuser=False,
        is_buyer=True,
        is_seller=False
    )
    db.add(db_user)
    db.flush()  # garante user_id

    # 3. Criar Buyer vinculado
    db_buyer = Buyer(
        user_id=db_user.user_id,
        preferences=buyer_data.preferences
    )
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    db.refresh(db_buyer, ['user'])  # carrega dados do user para o schema

    return db_buyer

    
def create_buyer_from_user(db: Session, buyer_data: BuyerCreate):
    """
    Cria um Buyer a partir de um User já existente.
    """
    # 1. Verificar se o User existe
    db_user = db.query(User).filter(User.user_id == buyer_data.user_id).first()
    if not db_user:
        raise ValueError("User não encontrado")
    
    # 2. Verificar se o User já é um Buyer
    existing_buyer = db.query(Buyer).filter(Buyer.user_id == buyer_data.user_id).first()
    if existing_buyer:
        raise ValueError("Este User já é um Buyer")
    
    
    # 4. Atualizar flags do User
    db_user.is_buyer = True
    db_user.is_seller = False
    
    # 5. Criar Buyer
    db_buyer = Buyer(
        user_id=db_user.user_id,
        preferences=buyer_data.preferences
    )
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    
    # 6. IMPORTANTE: Carregar o relacionamento user para o schema acessar
    db.refresh(db_buyer, ['user'])
    # OU usar joinedload na query:
    # db_buyer = db.query(Buyer).options(joinedload(Buyer.user)).filter(Buyer.buyer_id == db_buyer.buyer_id).first()
    
    return db_buyer


def create_or_update_preferences(preferences_data: BuyerUpdate,db: Session,buyer_id: int):
    """
    Cria ou atualiza preferences do buyer autenticado.
    Se o buyer não existir, cria. Se existir, atualiza.
    """
    # Verificar se o usuário é buyer
    db_user = db.query(User).filter(User.user_id == buyer_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User não encontrado")
    
    if not db_user.is_buyer:
        raise HTTPException(status_code=400, detail="Este usuário não é um Buyer")
    
    # Buscar buyer existente
    db_buyer = get_buyer_by_user_id(db, buyer_id)
    
    if db_buyer:
        # Se já existe, atualiza
        db_buyer.preferences = preferences_data.preferences
        db.commit()
        db.refresh(db_buyer)
        # Carregar relacionamento user
        db.refresh(db_buyer, ['user'])
        return db_buyer
    else:
        # Se não existe, cria
        db_buyer = Buyer(
            user_id=buyer_id,
            preferences=preferences_data.preferences
        )
        db.add(db_buyer)
        db.commit()
        db.refresh(db_buyer)
        # Carregar relacionamento user
        db.refresh(db_buyer, ['user'])
        return db_buyer

    """
    Cria um Buyer a partir de um User já existente.
    """
    # 1. Verificar se o User existe
    db_user = db.query(User).filter(User.user_id == buyer_data.user_id).first()
    if not db_user:
        raise ValueError("User não encontrado")
    
    # 2. Verificar se o User já é um Buyer
    existing_buyer = db.query(Buyer).filter(Buyer.user_id == buyer_data.user_id).first()
    if existing_buyer:
        raise ValueError("Este User já é um Buyer")
    
    
    # 4. Atualizar flags do User
    db_user.is_buyer = True
    db_user.is_seller = False
    
    # 5. Criar Buyer
    db_buyer = Buyer(
        user_id=db_user.user_id,
        preferences=buyer_data.preferences
    )
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    
    # 6. IMPORTANTE: Carregar o relacionamento user para o schema acessar
    db.refresh(db_buyer, ['user'])
    # OU usar joinedload na query:
    # db_buyer = db.query(Buyer).options(joinedload(Buyer.user)).filter(Buyer.buyer_id == db_buyer.buyer_id).first()
    
    return db_buyer


def alter_status_buyer(db: Session, buyer_id: int):
    """Deleta buyer (soft delete - marca como inativo)"""
    db_buyer = db.query(Buyer).filter(Buyer.buyer_id == buyer_id).first()
    
    if db_buyer is None:
        return None
    
    # Soft delete - marca o User como inativo
    db_buyer.is_active = False
    db.commit()
    db.refresh(db_buyer)
    return db_buyer


def delete_buyer_by_user_id(db: Session, user_id: int):
    """Deleta seller por user_id"""
    db_seller = db.query(Buyer).filter(Buyer.user_id == user_id).first()
    if not db_seller:
        raise HTTPException(status_code=404, detail="Seller não encontrado")
    db.delete(db_seller)





def get_buyer_by_user_id(db: Session, user_id: int):
    """Busca buyer pelo user_id com User carregado"""
    return db.query(Buyer).options(joinedload(Buyer.user)).filter(Buyer.user_id == user_id).first()