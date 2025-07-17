from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.usuario import Usuarios


class Clientes(Usuarios):
    __tablename__ = "clientes"

    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    preferencias = Column(String, nullable=False)
    status = Column(String)
    data_cadastro = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity': 'clientes'
    }