from sqlalchemy.orm import Session, joinedload
from app.models.seller import Seller
from app.models.user import User
from app.schemas.seller import SellerCreate, SellerCreateWithUser, SellerUpdate
from app.security.security import get_password_hash
from fastapi import HTTPException

def get_sellers(db: Session):
    """Retorna todos os sellers"""
    return db.query(Seller).options(joinedload(Seller.user)).all()


def get_seller(db: Session, seller_id: int):
    """Busca seller por seller_id"""
    return db.query(Seller).filter(Seller.seller_id == seller_id).first()


def create_seller(db: Session, seller_data: SellerCreateWithUser):
    """
    Cria um Seller com seu User associado.
    """
    # 1. Verificar se email/cnpj já existem
    if db.query(User).filter(User.email == seller_data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if db.query(User).filter(User.cnpj == seller_data.cnpj).first():
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    
    # 2. Criar User com is_seller=True
    db_user = User(
        full_name=seller_data.full_name,
        cpf=seller_data.cpf,
        email=seller_data.email,
        birthdate=seller_data.birthdate,
        gender=seller_data.gender,
        password=get_password_hash(seller_data.password),
        is_active=True,
        is_superuser=False,
        is_seller=True,
        is_buyer=False
    )
    db.add(db_user)
    db.flush()  # garante user_id

    # 3. Criar Seller vinculado
    db_seller = Seller(
        user_id=db_user.user_id,    
        store_name=seller_data.store_name,
        cnpj=seller_data.cnpj,
        description=seller_data.description
    )
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    db.refresh(db_seller, ['user'])  # carrega dados do user para o schema

    return db_seller


def create_seller_from_user(db: Session, seller_data: SellerCreate):
    """
    Cria um Seller a partir de um User já existente.
    """
    # 1. Verificar se o User existe
    db_user = db.query(User).filter(User.user_id == seller_data.user_id).first()
    if not db_user:
        raise ValueError("User não encontrado")
    
    # 2. Verificar se o User já é um Seller
    existing_seller = db.query(Seller).filter(Seller.user_id == seller_data.user_id).first()
    if existing_seller:
        raise ValueError("Este User já é um Seller")
    
    # 3. Verificar se o User já é um Seller
    if db_user.is_seller:
        raise ValueError("Este User já é um Seller")
    
    # 4. Atualizar flags do User
    db_user.is_seller = True
    db_user.is_buyer = False
    
    # 5. Criar Buyer
    db_seller = Seller(
        user_id=db_user.user_id,
        store_name=seller_data.store_name,
        cnpj=seller_data.cnpj,
        description=seller_data.description
    )
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    
    # 6. IMPORTANTE: Carregar o relacionamento user para o schema acessar
    db.refresh(db_seller, ['user'])
    # OU usar joinedload na query:
    # db_buyer = db.query(Buyer).options(joinedload(Buyer.user)).filter(Buyer.buyer_id == db_buyer.buyer_id).first()
    
    return db_seller


def create_or_update_preferences(seller_data: SellerUpdate,db: Session,seller_id: int):
    """
    Cria ou atualiza preferences do seller autenticado.
    Se o seller não existir, cria. Se existir, atualiza.
    """
    # Verificar se o usuário é buyer
    db_user = db.query(User).filter(User.user_id == seller_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User não encontrado")
    
    if not db_user.is_seller:
        raise HTTPException(status_code=400, detail="Este usuário não é um Seller")
    
    # Buscar buyer existente
    db_seller = get_seller_by_user_id(db, seller_id)
    
    if db_seller:
        # Se já existe, atualiza
        db_seller.store_name = seller_data.store_name
        db_seller.cnpj = seller_data.cnpj
        db_seller.description = seller_data.description
        db.commit()
        db.refresh(db_seller)
        # Carregar relacionamento user
        db.refresh(db_seller, ['user'])
        return db_seller
    else:
        # Se não existe, cria
        db_seller = Seller(
            user_id=seller_id,
            store_name=seller_data.store_name,
            cnpj=seller_data.cnpj,
            description=seller_data.description
        )
        db.add(db_seller)
        db.commit()
        db.refresh(db_seller)
        # Carregar relacionamento user
        db.refresh(db_seller, ['user'])
        return db_seller


def alter_status_seller(db: Session, seller_id: int):
    """Deleta seller (soft delete - marca como inativo)"""
    db_seller = db.query(Seller).filter(Seller.seller_id == seller_id).first()
    
    if db_seller is None:
        return None
    
    # Soft delete - marca o User como inativo
    db_seller.is_active = False
    db.commit()
    db.refresh(db_seller)
    return db_seller


def delete_seller_by_user_id(db: Session, user_id: int):
    """Deleta seller por user_id"""
    db_seller = db.query(Seller).filter(Seller.user_id == user_id).first()
    if not db_seller:
        raise HTTPException(status_code=404, detail="Seller não encontrado")
    db.delete(db_seller)








def get_seller_by_user_id(db: Session, user_id: int):
    """Busca seller pelo user_id"""
    return db.query(Seller).filter(Seller.user_id == user_id).first()


def get_seller_by_email(db: Session, email: str):
    """Busca seller pelo email"""
    user = db.query(User).filter(User.email == email, User.type == "seller").first()
    if user:
        return db.query(Seller).filter(Seller.user_id == user.user_id).first()
    return None


def check_email_exists(db: Session, email: str, exclude_user_id: int = None):
    """Verifica se um email já existe"""
    query = db.query(User).filter(User.email == email)
    if exclude_user_id:
        query = query.filter(User.user_id != exclude_user_id)
    return query.first() is not None


def check_cnpj_exists(db: Session, cnpj: str, exclude_seller_id: int = None):
    """Verifica se um CNPJ já existe"""
    query = db.query(Seller).filter(Seller.cnpj == cnpj)
    if exclude_seller_id:
        query = query.filter(Seller.seller_id != exclude_seller_id)
    return query.first() is not None