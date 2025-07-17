from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.usuario import Usuarios


class Vendedor(Usuarios):
    __tablename__ = "vendedor"
    id = Column(Integer, ForeignKey(Usuarios.id_usuario), primary_key=True, autoincrement=True)
    cnpj = Column(String(14), unique=True, index=True)
    descricao = Column(String, nullable=False)
    documentos = Column(String)
    status = Column(String) 
    data_cadastro = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity': 'vendedor'
    }