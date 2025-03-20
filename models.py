from sqlalchemy import Boolean, Integer, Column, ForeignKey, String, Float
from database import Base

class Shoes(Base):
    __tablename__ = 'shoes'
    
    id_shoe = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float, index=True)
    descricao = Column(String, index=True)
    quantidade = Column(Integer, index=True)
    
    