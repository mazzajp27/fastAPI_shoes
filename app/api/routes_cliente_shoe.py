from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.cliente_shoe import ClienteShoe
from app.models.shoes import Shoes
from app.models.usuario import Usuarios
from app.schemas.cliente_shoe import ClienteShoeResponse
from app.security.security import get_current_cliente, get_current_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cliente compra um tênis
@router.post("/cliente-shoe/{id_shoe}", response_model=ClienteShoeResponse)
def comprar_tenis(id_shoe: int, db: Session = Depends(get_db), current_cliente: Usuarios = Depends(get_current_cliente)):
    shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()
    if not shoe:
        raise HTTPException(status_code=404, detail="Tênis não encontrado")
    relacao = ClienteShoe(cliente_id=current_cliente.id, shoe_id=id_shoe)
    db.add(relacao)
    db.commit()
    db.refresh(relacao)
    return relacao

# Cliente vê suas compras
@router.get("/cliente-shoe/me", response_model=List[ClienteShoeResponse])
def minhas_compras(db: Session = Depends(get_db), current_cliente: Usuarios = Depends(get_current_cliente)):
    return db.query(ClienteShoe).filter(ClienteShoe.cliente_id == current_cliente.id).all()

# Admin vê todas as compras de um cliente
@router.get("/clientes/{cliente_id}/compras/", response_model=List[ClienteShoeResponse])
def read_cliente_compras(cliente_id: int, db: Session = Depends(get_db), current_admin: Usuarios = Depends(get_current_admin)):
    return db.query(ClienteShoe).filter(ClienteShoe.cliente_id == cliente_id).all()

# Admin vê todas as compras de um tênis
@router.get("/shoes/{shoe_id}/compras/", response_model=List[ClienteShoeResponse])
def read_shoe_compras(shoe_id: int, db: Session = Depends(get_db), current_admin: Usuarios = Depends(get_current_admin)):
    return db.query(ClienteShoe).filter(ClienteShoe.shoe_id == shoe_id).all() 