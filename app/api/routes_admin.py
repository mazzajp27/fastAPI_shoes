from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import admin as crud_admin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminResponse, AdminListResponse
from app.security.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admins/", status_code=HTTPStatus.CREATED, response_model=AdminResponse)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    novo_admin = crud_admin.create_admin(db, admin)
    return novo_admin

@router.get("/admins/", response_model=list[AdminListResponse])
def read_admins(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    admins = crud_admin.get_admins(db)
    if admins is None:
        raise HTTPException(status_code=404, detail="Nenhum admin encontrado")
    return admins

@router.get("/admins/{id}", response_model=AdminResponse)
def read_admin(id: int, db: Session = Depends(get_db)):
    db_admin = crud_admin.get_admin(db, id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return db_admin

@router.put("/admins/{id}", response_model=AdminResponse)
def update_admin(id: int, admin: AdminUpdate, db: Session = Depends(get_db)):
    db_admin = crud_admin.update_admin(db, id, admin)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return db_admin

@router.delete("/admins/{id}", response_model=AdminResponse)
def delete_admin(id:int, db: Session = Depends(get_db)):
    db_admin = crud_admin.delete_admin(db, id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin não encontrado")
    return db_admin 