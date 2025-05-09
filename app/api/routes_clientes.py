from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import clientes as crud_clientes
from app.schemas.clientes import ClientesCreate, ClientesUpdate, ClientesResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/clientes/", response_model=ClientesResponse)
def create_cliente(cliente: ClientesCreate, db: Session = Depends(get_db)):
    return crud_clientes.create_cliente(db, cliente)

@router.get("/clientes/", response_model=list[ClientesResponse])
def read_clientes(db: Session = Depends(get_db)):
    return crud_clientes.get_clientes(db)

@router.get("/clientes/{id_cliente}", response_model=ClientesResponse)
def read_shoe(id_cliente: str, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

@router.put("/clientes/{id_cliente}", response_model=ClientesResponse)
def update_cliente(id_cliente: str, cliente: ClientesUpdate, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.update_cliente(db, id_cliente, cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente