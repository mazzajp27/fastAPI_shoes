# app/crud/shoes.py

from sqlalchemy.orm import Session
from app.models.shoes import Shoes
from app.schemas.shoes import ShoesCreate, ShoesUpdate

def create_shoe(db: Session, shoe: ShoesCreate):
    db_shoe = Shoes(**shoe.dict())
    db.add(db_shoe)
    db.commit()
    db.refresh(db_shoe)
    return db_shoe

def get_shoes(db: Session):
    return db.query(Shoes).all()

def get_shoe(db: Session, id_shoe: int):
    return db.query(Shoes).filter(Shoes.id == id_shoe).first()

def update_shoe(db: Session, id_shoe: int, shoe: ShoesUpdate):
    db_shoe = db.query(Shoes).filter(Shoes.id == id_shoe).first()
    if db_shoe:
        for key, value in shoe.dict(exclude_unset=True).items():
            setattr(db_shoe, key, value)
        db.commit()
        db.refresh(db_shoe)
    return db_shoe
