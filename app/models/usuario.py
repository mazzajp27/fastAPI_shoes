from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base
from datetime import datetime


class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    telefone = Column(String, unique=True, nullable=False)
    endereco = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    genero = Column(String, nullable=False) 
    data_nascimento = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)
    status = Column(String, nullable=False)
    data_cadastro = Column(Date, default=datetime.utcnow)
    
    __mapper_args__ = {
        'polymorphic_identity': 'usuarios',
        'polymorphic_on': 'tipo'
    }
