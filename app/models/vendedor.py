from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.usuario import Usuarios
from datetime import datetime


class Vendedor(Usuarios):
    __tablename__ = "vendedor"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    cnpj = Column(String(14), unique=True, index=True)
    descricao = Column(String, nullable=False)
    documentos = Column(String)
    status = Column(String) 
    data_cadastro = Column(Date, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'vendedor'
    }