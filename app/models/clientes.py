from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Clientes(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(14), unique=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    genero = Column(String) 
    data_nascimento = Column(Date)

    # Relacionamento com compras
    cliente_shoes = relationship("ClienteShoe", back_populates="clientes")