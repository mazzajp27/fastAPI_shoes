from sqlalchemy.orm import Session
from app.models.admin import Administrador
from app.schemas.admin import AdminCreate, AdminUpdate
from app.security.security import get_password_hash, verify_password
from app.models.usuario import Usuarios

def create_admin(db: Session, admin: AdminCreate):
    db_admin = Administrador(**admin.dict())
    db_admin.tipo = "administrador"
    db_admin.status = "ativo"
    db_admin.senha = get_password_hash(db_admin.senha)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admins(db: Session):
    return db.query(Usuarios).filter(Usuarios.tipo == "administrador").all()

def get_admin(db: Session, id: int):
    """Busca admin por ID, funcionando com herança de tabelas"""
    admin = db.query(Administrador).filter(Administrador.id == id).first()
    if not admin:
        usuario = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "administrador").first()
        if usuario:
            return usuario
    return admin

def update_admin(db: Session, id: int, admin: AdminUpdate):
    """Atualiza admin por ID, funcionando com herança de tabelas"""
    db_admin = db.query(Administrador).filter(Administrador.id == id).first()
    if not db_admin:
        db_admin = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "administrador").first()
    if db_admin:
        update_data = admin.dict(exclude_unset=True)
        if "senha" in update_data:
            update_data["senha"] = get_password_hash(update_data["senha"])
        for key, value in update_data.items():
            setattr(db_admin, key, value)
        db.commit()
        db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, id: int):
    """Soft delete admin por ID, funcionando com herança de tabelas"""
    db_admin = db.query(Administrador).filter(Administrador.id == id).first()
    if not db_admin:
        db_admin = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "administrador").first()
    if db_admin is None:
        return None
    db_admin.status = "inativo"
    db.commit()
    db.refresh(db_admin)
    return db_admin

def login_admin(db: Session, email: str, senha: str):
    admin = db.query(Administrador).filter(Administrador.email == email).first()
    if not admin:
        return None
    if admin.status != "ativo":
        return None
    if not verify_password(senha, admin.senha):
        return None
    return admin

def get_admin_by_user_id(db: Session, user_id: int):
    admin = db.query(Administrador).filter(Administrador.id == user_id).first()
    if not admin:
        usuario = db.query(Usuarios).filter(Usuarios.id == user_id).first()
        if usuario and usuario.tipo == "administrador":
            return usuario
    return admin

def get_admin_by_email(db: Session, email: str):
    return db.query(Administrador).filter(Administrador.email == email).first()

def check_email_exists(db: Session, email: str, exclude_id: int = None):
    query = db.query(Usuarios).filter(Usuarios.email == email)
    if exclude_id:
        query = query.filter(Usuarios.id != exclude_id)
    return query.first() is not None

def check_cpf_exists(db: Session, cpf: str, exclude_id: int = None):
    query = db.query(Usuarios).filter(Usuarios.cpf == cpf)
    if exclude_id:
        query = query.filter(Usuarios.id != exclude_id)
    return query.first() is not None 