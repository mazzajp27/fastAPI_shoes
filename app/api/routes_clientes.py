from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import clientes as crud_clientes
from app.schemas.clientes import ClienteCreate, ClienteUpdate, ClienteResponse, ClienteListResponse
from app.security.security import get_current_user, get_current_cliente, get_current_admin
from app.models.usuario import Usuarios
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

@router.post("/clientes/register", status_code=HTTPStatus.CREATED, response_model=ClienteResponse)
def register_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registro de novos clientes
    """
    # Verificar se já existe um usuário com este email
    existing_user = db.query(Usuarios).filter(Usuarios.email == cliente.email).first()
    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário cadastrado com este email"
        )
    
    # Verificar se já existe um usuário com este CPF
    existing_cpf = db.query(Usuarios).filter(Usuarios.cpf == cliente.cpf).first()
    if existing_cpf:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário cadastrado com este CPF"
        )
    
    # Verificar se já existe um usuário com este telefone
    existing_phone = db.query(Usuarios).filter(Usuarios.telefone == cliente.telefone).first()
    if existing_phone:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário cadastrado com este telefone"
        )
    
    novo_cliente = crud_clientes.create_cliente(db, cliente)
    return validar_resposta_cliente(novo_cliente)



# Rotas para clientes acessarem seus próprios dados
@router.get("/clientes/me", response_model=ClienteResponse)
def read_me(current_user: Usuarios = Depends(get_current_cliente), db: Session = Depends(get_db)):
    # Buscar o cliente completo na tabela clientes para ter acesso ao campo preferencias
    db_cliente = crud_clientes.get_cliente(db, current_user.id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)

@router.put("/clientes/me", response_model=ClienteResponse)
def update_me(cliente: ClienteUpdate, current_user: Usuarios = Depends(get_current_cliente), db: Session = Depends(get_db)):
    db_cliente = crud_clientes.update_cliente(db, current_user.id, cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)

@router.delete("/clientes/me", response_model=ClienteResponse)
def delete_me(current_user: Usuarios = Depends(get_current_cliente), db: Session = Depends(get_db)):
    db_cliente = crud_clientes.delete_cliente(db, current_user.id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

# Rotas administrativas (apenas para administradores)
@router.get("/clientes/", response_model=list[ClienteListResponse])
def read_all_clientes(db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    clientes = crud_clientes.get_clientes(db)
    if clientes is None:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado")
    return clientes

@router.get("/clientes/{id}", response_model=ClienteResponse)
def read_cliente(id: int, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_cliente = crud_clientes.get_cliente(db, id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)

@router.put("/clientes/{id}", response_model=ClienteResponse)
def update_cliente(id: int, cliente: ClienteUpdate, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_cliente = crud_clientes.update_cliente(db, id, cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return validar_resposta_cliente(db_cliente)

@router.delete("/clientes/{id}", response_model=ClienteResponse)
def delete_cliente(id: int, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_cliente = crud_clientes.delete_cliente(db, id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente