from sqlalchemy.orm import Session
from app.models.vendedor import Vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate

def create_vendedor(db: Session, vendedor: VendedorCreate):
    db_vendedor = Vendedor(**vendedor.dict())
    db_vendedor.tipo = "vendedor"  
    db_vendedor.status = "ativo"
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def get_vendedores(db: Session):
    return db.query(Vendedor).all()

def get_vendedor(db: Session, id: int):
    return db.query(Vendedor).filter(Vendedor.id == id).first()

def update_vendedor(db: Session, id: int, vendedor: VendedorUpdate):
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if db_vendedor:
        for key, value in vendedor.dict(exclude_unset=True).items():
            setattr(db_vendedor, key, value)
        db.commit()
        db.refresh(db_vendedor)
    return db_vendedor

def delete_vendedor(db: Session, id: int):
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if db_vendedor is None:
        return None
    db.delete(db_vendedor)
    db.commit()
    return db_vendedor 