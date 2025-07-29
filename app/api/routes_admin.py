from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import admin as crud_admin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminResponse, AdminListResponse
from app.security.security import get_current_user, get_current_admin
from app.models.usuario import Usuarios
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validar_resposta_admin(admin: AdminResponse):
    if not admin.nome or not admin.email:
        raise HTTPException(status_code=500, detail="Dados inválidos retornados do banco")
    return admin

@router.post("/admins/register", status_code=HTTPStatus.CREATED, response_model=AdminResponse)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registro de novos administradores
    """
    # Verificar se já existe um usuário com este email
    if crud_admin.check_email_exists(db, admin.email):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuário cadastrado com este email")
    # Verificar se já existe um usuário com este CPF
    if crud_admin.check_cpf_exists(db, admin.cpf):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuário cadastrado com este CPF")
    # Verificar se já existe um usuário com este telefone
    existing_phone = db.query(Usuarios).filter(Usuarios.telefone == admin.telefone).first()
    if existing_phone:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuário cadastrado com este telefone")
    novo_admin = crud_admin.create_admin(db, admin)
    return validar_resposta_admin(novo_admin)

# Rotas para administradores acessarem seus próprios dados
@router.get("/admins/me", response_model=AdminResponse)
def read_me(current_user: Usuarios = Depends(get_current_admin), db: Session = Depends(get_db)):
    db_admin = crud_admin.get_admin(db, current_user.id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return validar_resposta_admin(db_admin)

@router.put("/admins/me", response_model=AdminResponse)
def update_me(admin: AdminUpdate, current_user: Usuarios = Depends(get_current_admin), db: Session = Depends(get_db)):
    db_admin = crud_admin.update_admin(db, current_user.id, admin)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return validar_resposta_admin(db_admin)

@router.delete("/admins/me", response_model=AdminResponse)
def delete_me(current_user: Usuarios = Depends(get_current_admin), db: Session = Depends(get_db)):
    db_admin = crud_admin.delete_admin(db, current_user.id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return db_admin

# Rotas administrativas (apenas para administradores)
@router.get("/admins/", response_model=list[AdminListResponse])
def read_admins(db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    admins = crud_admin.get_admins(db)
    if admins is None:
        raise HTTPException(status_code=404, detail="Nenhum admin encontrado")
    return admins

@router.get("/admins/{id}", response_model=AdminResponse)
def read_admin(id: int, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_admin = crud_admin.get_admin(db, id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return validar_resposta_admin(db_admin)

@router.put("/admins/{id}", response_model=AdminResponse)
def update_admin(id: int, admin: AdminUpdate, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_admin = crud_admin.update_admin(db, id, admin)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return validar_resposta_admin(db_admin)

@router.delete("/admins/{id}", response_model=AdminResponse)
def delete_admin(id:int, db: Session = Depends(get_db), current_user: Usuarios = Depends(get_current_admin)):
    db_admin = crud_admin.delete_admin(db, id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return db_admin 