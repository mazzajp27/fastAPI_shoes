from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Shoes(Base):
    __tablename__ = "shoes"

    id_shoe = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    descricao = Column(String, nullable=True)
    quantidade = Column(Integer, nullable=True)
    imagem = Column(String, nullable=True)
    marca = Column(String)
    modelo = Column(String)
    tamanho = Column(Integer)
    cor = Column(String)
    vendedor_id = Column(Integer, ForeignKey("vendedor.id"))
    
    
    
    vendedor = relationship("Vendedor", back_populates="shoes")
    cliente_shoes = relationship("ClienteShoe", back_populates="shoes")
    