from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import clientes as crud_clientes
from app.schemas.clientes import ClienteCreate, ClienteUpdate, ClienteResponse, ClienteListResponse
from app.security.security import get_current_user
from datetime import date


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validar_resposta_cliente(cliente: ClienteResponse):
    if not cliente.nome or not cliente.email:
        raise HTTPException(status_code=500, detail="Dados inválidos retornados do banco")
    return cliente


@router.post("/clientes/", status_code=HTTPStatus.CREATED, response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = crud_clientes.create_cliente(db, cliente)
    return validar_resposta_cliente(novo_cliente)

@router.get("/clientes/", response_model=list[ClienteListResponse])
def read_clientes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    clientes = crud_clientes.get_clientes(db)
    if clientes is None:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado")
    return clientes

@router.get("/clientes/{id}", response_model=ClienteResponse)
def read_cliente(id: int, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.get_cliente(db, id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)


@router.put("/clientes/{id}", response_model=ClienteResponse)
def update_cliente(id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.update_cliente(db, id, cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)

@router.delete("/clientes/{id}", response_model=ClienteResponse)
def delete_cliente(id: int, db: Session = Depends(get_db)):
    db_cliente = crud_clientes.delete_cliente(db, id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente