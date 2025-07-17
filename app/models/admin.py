from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.usuario import Usuarios


class Administrador(Usuarios):
    __tablename__ = "administrador"

    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    nivel_acesso = Column(String, nullable=False)
    status = Column(String)
    data_cadastro = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity': 'administrador'
    }