from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Shoes(Base):
    __tablename__ = "shoes"

    id_shoe = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    descricao = Column(String)
    quantidade = Column(Integer)
