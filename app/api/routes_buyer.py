from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import buyer as crud_buyer
from app.schemas.buyer import BuyerBase, BuyerCreateWithUser, BuyerDisplay, BuyerUpdate, BuyerCreate
from app.security.security import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/buyers/", response_model=list[BuyerDisplay])
def read_all_buyers(db: Session = Depends(get_db)):
    """Lista todos os buyers (pode adicionar autenticação depois)"""
    buyers = crud_buyer.get_buyers(db)
    return buyers


@router.get("/buyers/{buyer_id}", response_model=BuyerDisplay)
def read_buyer(buyer_id: int, db: Session = Depends(get_db)):
    """Busca buyer por ID"""
    db_buyer = crud_buyer.get_buyer(db, buyer_id)
    if db_buyer is None:
        raise HTTPException(status_code=404, detail="Buyer não encontrado")
    return db_buyer


@router.post("/buyers/register", status_code=HTTPStatus.CREATED, response_model=BuyerDisplay)
def register_buyer(buyer: BuyerCreateWithUser, db: Session = Depends(get_db)):
    """
    Endpoint para registro de novos buyers.
    Recebe dados do User + Buyer e cria ambos.
    """
    novo_buyer = crud_buyer.create_buyer(db, buyer)
    return novo_buyer


@router.post("/buyers/from-user/{user_id}", status_code=HTTPStatus.CREATED, response_model=BuyerDisplay)
def create_buyer_from_user(user_id: int,buyer: BuyerCreate,db: Session = Depends(get_db)):
    """
    Converte um User existente em Buyer.
    Recebe apenas os campos específicos do Buyer.
    """
    buyer_data = BuyerCreate(
        user_id=user_id,
        preferences=buyer.preferences
    )
    
    try:
        # Cria um Buyer a partir de um User já existente
        novo_buyer = crud_buyer.create_buyer_from_user(db, buyer_data)
        return novo_buyer
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


@router.put("/buyers/{user_id}", response_model=BuyerDisplay)
def update_buyer_by_user_id(user_id: int,buyer: BuyerUpdate,db: Session = Depends(get_db)):
    """
    Atualiza as informações específicas do Buyer a partir do user_id.
    Se o buyer ainda não existir, cria com os dados enviados.
    """
    return crud_buyer.create_or_update_preferences(
        preferences_data=buyer,
        db=db,
        buyer_id=user_id,
    )


@router.delete("/buyers/alter-status/{user_id}", response_model=BuyerDisplay)
def alter_status_buyer(user_id: int,db: Session = Depends(get_db)):
    """Delete buyer por user_id"""
    return crud_buyer.alter_status_buyer(db, user_id)


@router.delete("/buyers/{user_id}", response_model=BuyerDisplay)
def delete_buyer_by_user_id(user_id: int,db: Session = Depends(get_db)):
    """Deleta buyer por user_id"""
    return crud_buyer.delete_buyer_by_user_id(db, user_id)









@router.get("/buyers/me", response_model=BuyerDisplay)
def read_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retorna dados do buyer autenticado"""
    db_buyer = crud_buyer.get_buyer_by_user_id(db, current_user.user_id)
    if db_buyer is None:
        raise HTTPException(status_code=404, detail="Buyer não encontrado")
    return db_buyer


@router.put("/buyers/me", response_model=BuyerDisplay)
def update_me(buyer: BuyerUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """Atualiza dados do buyer autenticado"""
    db_buyer = crud_buyer.get_buyer_by_user_id(db, current_user.user_id)
    if db_buyer is None:
        raise HTTPException(status_code=404, detail="Buyer não encontrado")
    
    updated_buyer = crud_buyer.update_buyer(db, db_buyer.buyer_id, buyer)
    return updated_buyer



@router.delete("/buyers/me", response_model=BuyerDisplay)
def delete_me(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """Deleta buyer autenticado (soft delete)"""
    db_buyer = crud_buyer.get_buyer_by_user_id(db, current_user.user_id)
    if db_buyer is None:
        raise HTTPException(status_code=404, detail="Buyer não encontrado")
    
    return crud_buyer.delete_buyer(db, db_buyer.buyer_id)

