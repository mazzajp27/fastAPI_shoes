from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
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

def validar_resposta_cliente(cliente: ClientesResponse):
    if not cliente.nome or not cliente.email:
        raise HTTPException(status_code=500, detail="Dados inválidos retornados do banco")
    return cliente

@router.post("/clientes/", status_code=HTTPStatus.CREATED, response_model=ClientesResponse)
def create_cliente(cliente: ClientesCreate, db: Session = Depends(get_db)):
    novo_cliente = crud_clientes.create_cliente(db, cliente)
    return validar_resposta_cliente(novo_cliente)

@router.get("/clientes/", response_model=list[ClientesResponse])
def read_clientes(db: Session = Depends(get_db)):
    clientes = crud_clientes.get_clientes(db)
    for cliente in clientes:
        validar_resposta_cliente(cliente)
    return clientes

@router.get("/clientes/{id_cliente}", response_model=ClientesResponse)
def read_cliente(id_cliente: str, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.get_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)

@router.put("/clientes/{id_cliente}", response_model=ClientesResponse)
def update_cliente(id_cliente: str, cliente: ClientesUpdate, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.update_cliente(db, id_cliente, cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)

@router.delete("/clientes/{id_cliente}", response_model=ClientesResponse)
def delete_cliente(id_cliente:int, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.delete_cliente(db, id_cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente
