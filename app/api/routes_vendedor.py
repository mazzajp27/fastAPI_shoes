from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import vendedor as crud_vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate, VendedorResponse, VendedorListResponse
from app.security.security import get_current_user, get_current_vendedor, get_current_admin
from app.models.usuario import Usuarios
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validar_resposta_vendedor(vendedor: VendedorResponse):
    if not vendedor.nome or not vendedor.email:
        raise HTTPException(status_code=500, detail="Dados inválidos retornados do banco")
    return vendedor

@router.post("/vendedores/register", status_code=HTTPStatus.CREATED, response_model=VendedorResponse)
def register_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registro de novos vendedores
    """
    # Verificar se já existe um usuário com este email
    existing_user = db.query(Usuarios).filter(Usuarios.email == vendedor.email).first()
    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário cadastrado com este email"
        )
    
    # Verificar se já existe um usuário com este CPF
    existing_cpf = db.query(Usuarios).filter(Usuarios.cpf == vendedor.cpf).first()
    if existing_cpf:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário cadastrado com este CPF"
        )
    
    # Verificar se já existe um usuário com este telefone
    existing_phone = db.query(Usuarios).filter(Usuarios.telefone == vendedor.telefone).first()
    if existing_phone:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário cadastrado com este telefone"
        )
    
    # Verificar se já existe um vendedor com este CNPJ
    existing_cnpj = crud_vendedor.check_cnpj_exists(db, vendedor.cnpj)
    if existing_cnpj:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um vendedor cadastrado com este CNPJ"
        )
    
    novo_vendedor = crud_vendedor.create_vendedor(db, vendedor)
    return validar_resposta_vendedor(novo_vendedor)

# Rotas para vendedores acessarem seus próprios dados
@router.get("/vendedores/me", response_model=VendedorResponse)
def read_me(current_user: Usuarios = Depends(get_current_vendedor), db: Session = Depends(get_db)):
    # Buscar o vendedor completo na tabela vendedor para ter acesso aos campos específicos
    db_vendedor = crud_vendedor.get_vendedor(db, current_user.id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return validar_resposta_vendedor(db_vendedor)

@router.put("/vendedores/me", response_model=VendedorResponse)
def update_me(vendedor: VendedorUpdate, current_user: Usuarios = Depends(get_current_vendedor), db: Session = Depends(get_db)):
    db_vendedor = crud_vendedor.update_vendedor(db, current_user.id, vendedor)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return validar_resposta_vendedor(db_vendedor)

@router.delete("/vendedores/me", response_model=VendedorResponse)
def delete_me(current_user: Usuarios = Depends(get_current_vendedor), db: Session = Depends(get_db)):
    db_vendedor = crud_vendedor.delete_vendedor(db, current_user.id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return db_vendedor

# Rotas administrativas (apenas para administradores)
@router.get("/vendedores/", response_model=list[VendedorListResponse])
def read_all_vendedores(db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    vendedores = crud_vendedor.get_vendedores(db)
    if vendedores is None:
        raise HTTPException(status_code=404, detail="Nenhum vendedor encontrado")
    return vendedores

@router.get("/vendedores/{id}", response_model=VendedorResponse)
def read_vendedor(id: int, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_vendedor = crud_vendedor.get_vendedor(db, id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return validar_resposta_vendedor(db_vendedor)

@router.put("/vendedores/{id}", response_model=VendedorResponse)
def update_vendedor(id: int, vendedor: VendedorUpdate, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_vendedor = crud_vendedor.update_vendedor(db, id, vendedor)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return validar_resposta_vendedor(db_vendedor)

@router.delete("/vendedores/{id}", response_model=VendedorResponse)
def delete_vendedor(id: int, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_vendedor = crud_vendedor.delete_vendedor(db, id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return db_vendedor 