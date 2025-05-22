# app/crud/shoes.py

from sqlalchemy.orm import Session
from app.models.shoes import Shoes
from app.models.cliente_shoe import ClienteShoe
from app.schemas.shoes import ShoesCreate, ShoesUpdate

def create_shoe(db: Session, shoe: ShoesCreate):
    # Extrair o cliente_id do schema
    cliente_id = shoe.cliente_id
    shoe_data = shoe.dict(exclude={'cliente_id'})
    
    # Criar o tênis
    db_shoe = Shoes(**shoe_data)
    db.add(db_shoe)
    db.commit()
    db.refresh(db_shoe)
    
    # Criar o relacionamento
    cliente_shoe = ClienteShoe(cliente_id=cliente_id, shoe_id=db_shoe.id_shoe)
    db.add(cliente_shoe)
    db.commit()
    
    return db_shoe

def get_shoes(db: Session):
    return db.query(Shoes).all()

def get_shoe(db: Session, id_shoe: int):
    return db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()

def update_shoe(db: Session, id_shoe: int, shoe: ShoesUpdate):
    db_shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()
    if db_shoe:
        for key, value in shoe.dict(exclude_unset=True).items():
            setattr(db_shoe, key, value)
        db.commit()
        db.refresh(db_shoe)
    return db_shoe

def delete_shoe(db: Session, id_shoe: int):
    db_shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()
    if db_shoe is None:
        return None
    db.delete(db_shoe)
    db.commit()
    return db_shoe