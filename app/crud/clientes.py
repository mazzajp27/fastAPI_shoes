# app/crud/clientes.py

from sqlalchemy.orm import Session
from app.models.clientes import Clientes
from app.schemas.clientes import ClientesCreate, ClientesUpdate

def create_cliente(db: Session, cliente: ClientesCreate):
    db_cliente = Clientes(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_clientes(db: Session):
    return db.query(Clientes).all()

def get_cliente(db: Session, id_cliente: str):
    return db.query(Clientes).filter(Clientes.id_cliente == id_cliente).first()

def update_cliente(db: Session, id_cliente: str, cliente: ClientesUpdate):
    db_cliente = db.query(Clientes).filter(Clientes.id_cliente == id_cliente).first()
    if db_cliente:
        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, id_cliente: int):
    db_cliente = db.query(Clientes).filter(Clientes.id_cliente == id_cliente).first()
    if db_cliente is None:
        return None
    db.delete(db_cliente)
    db.commit()
    return db_cliente