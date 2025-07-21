from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import usuario as crud_usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuarios/", status_code=HTTPStatus.CREATED, response_model=UsuarioResponse)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = crud_usuario.create_usuario(db, usuario)
    return novo_usuario

@router.get("/usuarios/", response_model=list[UsuarioResponse])
def read_usuarios(db: Session = Depends(get_db)):
    return crud_usuario.get_usuarios(db)

@router.get("/usuarios/{id}", response_model=UsuarioResponse)
def read_usuario(id: int, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario(db, id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.put("/usuarios/{id}", response_model=UsuarioResponse)
def update_usuario(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.update_usuario(db, id, usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.delete("/usuarios/{id}", response_model=UsuarioResponse)
def delete_usuario(id:int, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.delete_usuario(db, id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario 