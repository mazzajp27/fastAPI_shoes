from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.cliente_shoe import ClienteShoe
from app.schemas.cliente_shoe import ClienteShoeCreate, ClienteShoeResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cliente-shoe/", response_model=ClienteShoeResponse)
def create_cliente_shoe(cliente_shoe: ClienteShoeCreate, db: Session = Depends(get_db)):
    db_cliente_shoe = ClienteShoe(
        cliente_id=cliente_shoe.cliente_id,
        shoe_id=cliente_shoe.shoe_id
    )
    db.add(db_cliente_shoe)
    db.commit()
    db.refresh(db_cliente_shoe)
    return db_cliente_shoe

@router.get("/cliente-shoe/", response_model=List[ClienteShoeResponse])
def read_cliente_shoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cliente_shoes = db.query(ClienteShoe).offset(skip).limit(limit).all()
    return cliente_shoes

@router.get("/cliente-shoe/{cliente_shoe_id}", response_model=ClienteShoeResponse)
def read_cliente_shoe(cliente_shoe_id: int, db: Session = Depends(get_db)):
    db_cliente_shoe = db.query(ClienteShoe).filter(ClienteShoe.id == cliente_shoe_id).first()
    if db_cliente_shoe is None:
        raise HTTPException(status_code=404, detail="ClienteShoe not found")
    return db_cliente_shoe

@router.get("/clientes/{cliente_id}/compras/", response_model=List[ClienteShoeResponse])
def read_cliente_compras(cliente_id: int, db: Session = Depends(get_db)):
    compras = db.query(ClienteShoe).filter(ClienteShoe.cliente_id == cliente_id).all()
    return compras

@router.get("/shoes/{shoe_id}/compras/", response_model=List[ClienteShoeResponse])
def read_shoe_compras(shoe_id: int, db: Session = Depends(get_db)):
    compras = db.query(ClienteShoe).filter(ClienteShoe.shoe_id == shoe_id).all()
    return compras 