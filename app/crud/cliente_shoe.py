from sqlalchemy.orm import Session
from app.models.cliente_shoe import ClienteShoe
from app.schemas.cliente_shoe import ClienteShoeCreate

def create_cliente_shoe(db: Session, cliente_shoe: ClienteShoeCreate):
    db_cliente_shoe = ClienteShoe(**cliente_shoe.model_dump())
    db.add(db_cliente_shoe)
    db.commit()
    db.refresh(db_cliente_shoe)
    return db_cliente_shoe

def get_cliente_shoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClienteShoe).offset(skip).limit(limit).all()

def get_cliente_shoe(db: Session, cliente_shoe_id: int):
    return db.query(ClienteShoe).filter(ClienteShoe.id == cliente_shoe_id).first()

def get_cliente_compras(db: Session, cliente_id: int):
    return db.query(ClienteShoe).filter(ClienteShoe.cliente_id == cliente_id).all()

def get_shoe_compras(db: Session, shoe_id: int):
    return db.query(ClienteShoe).filter(ClienteShoe.shoe_id == shoe_id).all() 