from sqlalchemy.orm import Session
from app.models.usuario import Usuarios
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.security.security import get_password_hash

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuarios(**usuario.dict())
    db_usuario.senha = get_password_hash(db_usuario.senha)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuarios(db: Session):
    return db.query(Usuarios).all()

def get_usuario(db: Session, id: int):
    return db.query(Usuarios).filter(Usuarios.id == id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuarios).filter(Usuarios.email == email).first()

def update_usuario(db: Session, id: int, usuario: UsuarioUpdate):
    db_usuario = db.query(Usuarios).filter(Usuarios.id == id).first()
    if db_usuario:
        for key, value in usuario.dict(exclude_unset=True).items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, id: int):
    db_usuario = db.query(Usuarios).filter(Usuarios.id == id).first()
    if db_usuario is None:
        return None
    db.delete(db_usuario)
    db.commit()
    return db_usuario 