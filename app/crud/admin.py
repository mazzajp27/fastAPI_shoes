from sqlalchemy.orm import Session
from app.models.admin import Administrador
from app.schemas.admin import AdminCreate, AdminUpdate

def create_admin(db: Session, admin: AdminCreate):
    db_admin = Administrador(**admin.dict())
    db_admin.tipo = "administrador"
    db_admin.status = "ativo"
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admins(db: Session):
    return db.query(Administrador).all()

def get_admin(db: Session, id: int):
    return db.query(Administrador).filter(Administrador.id == id).first()

def update_admin(db: Session, id: int, admin: AdminUpdate):
    db_admin = db.query(Administrador).filter(Administrador.id == id).first()
    if db_admin:
        for key, value in admin.dict(exclude_unset=True).items():
            setattr(db_admin, key, value)
        db.commit()
        db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, id: int):
    db_admin = db.query(Administrador).filter(Administrador.id == id).first()
    if db_admin is None:
        return None
    db.delete(db_admin)
    db.commit()
    return db_admin 