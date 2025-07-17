from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base


class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(14), unique=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    endereco = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    genero = Column(String) 
    data_nascimento = Column(Date)
    tipo = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity': 'usuarios',
        'polymorphic_on': 'tipo'
    }
