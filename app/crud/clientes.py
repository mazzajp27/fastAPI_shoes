# app/crud/clientes.py

from sqlalchemy.orm import Session
from app.models.clientes import Clientes
from app.schemas.clientes import ClienteCreate, ClienteUpdate

def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Clientes(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_clientes(db: Session):
    return db.query(Clientes).all()

def get_cliente(db: Session, id: int):
    return db.query(Clientes).filter(Clientes.id == id).first()

def update_cliente(db: Session, id: int, cliente: ClienteUpdate):
    db_cliente = db.query(Clientes).filter(Clientes.id == id).first()
    if db_cliente:
        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, id: int):
    db_cliente = db.query(Clientes).filter(Clientes.id == id).first()
    if db_cliente is None:
        return None
    db.delete(db_cliente)
    db.commit()
    return db_cliente

def login_cliente(db: Session, email: str, senha: str):
    cliente = db.query(Clientes).filter(Clientes.email == email).first()
    if not cliente:
        return None
    if cliente.senha != senha:  # Em produção, use hash de senha!
        return None
    return cliente