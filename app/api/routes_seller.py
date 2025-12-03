from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import seller as crud_seller
from app.schemas.seller import SellerCreateWithUser, SellerDisplay, SellerUpdate, SellerCreate
from app.security.security import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/sellers/", response_model=list[SellerDisplay])
def read_all_sellers(db: Session = Depends(get_db)):
    """List all sellers """
    sellers = crud_seller.get_sellers(db)
    return sellers


@router.get("/sellers/{seller_id}", response_model=SellerDisplay)
def read_seller(seller_id: int, db: Session = Depends(get_db)):
    """Search seller by ID"""
    db_seller = crud_seller.get_seller(db, seller_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller não encontrado")
    return db_seller


@router.post("/sellers/register", status_code=HTTPStatus.CREATED, response_model=SellerDisplay)
def register_seller(seller: SellerCreateWithUser, db: Session = Depends(get_db)):
    """
    Register new sellers.
    Receive User and Seller data and create both.
    """
    novo_seller = crud_seller.create_seller(db, seller)
    return novo_seller


@router.post("/sellers/from-user/{user_id}", status_code=HTTPStatus.CREATED, response_model=SellerDisplay)
def create_seller_from_user(user_id: int,seller: SellerCreate,db: Session = Depends(get_db)):
    """
    Converte um User existente em Seller.
    Recebe apenas os campos específicos do Seller.
    """
    seller_data = SellerCreate(
        user_id=user_id,
        store_name=seller.store_name,
        cnpj=seller.cnpj,
        description=seller.description
    )
    
    try:
        novo_seller = crud_seller.create_seller_from_user(db, seller_data)
        return novo_seller
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


@router.put("/sellers/{user_id}", response_model=SellerDisplay)
def update_seller_by_user_id(user_id: int,seller: SellerUpdate,db: Session = Depends(get_db)):
    """
    Atualiza as informações específicas do Seller a partir do user_id.
    Se o seller ainda não existir, cria com os dados enviados.
    """
    return crud_seller.create_or_update_preferences(
        seller_data=seller,
        db=db,
        seller_id=user_id,
    )


@router.delete("/sellers/alter-status/{user_id}", response_model=SellerDisplay)
def alter_status_seller(user_id: int,db: Session = Depends(get_db)):
    """Deleta seller por user_id"""
    return crud_seller.alter_status_seller(db, user_id)


@router.delete("/sellers/{user_id}", response_model=SellerDisplay)
def delete_seller_by_user_id(user_id: int,db: Session = Depends(get_db)):
    """Deleta seller por user_id"""
    return crud_seller.delete_seller_by_user_id(db, user_id)






@router.get("/sellers/me", response_model=SellerDisplay)
def read_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retorna dados do seller autenticado"""
    db_seller = crud_seller.get_seller_by_user_id(db, current_user.user_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller não encontrado")
    return db_seller


@router.put("/sellers/me", response_model=SellerDisplay)
def update_me(
    seller: SellerUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Atualiza dados do seller autenticado"""
    db_seller = crud_seller.get_seller_by_user_id(db, current_user.user_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller não encontrado")
    
    updated_seller = crud_seller.update_seller(db, db_seller.seller_id, seller)
    return updated_seller


@router.delete("/sellers/me", response_model=SellerDisplay)
def delete_me(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Deleta seller autenticado (soft delete)"""
    db_seller = crud_seller.get_seller_by_user_id(db, current_user.user_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller não encontrado")
    
    return crud_seller.delete_seller(db, db_seller.seller_id)

