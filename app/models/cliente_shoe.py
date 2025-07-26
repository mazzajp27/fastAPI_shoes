from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.clientes import Clientes

class ClienteShoe(Base):
    __tablename__ = "cliente_shoes"

    id_compra = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = Column(Integer, ForeignKey("clientes.id"))
    shoe_id = Column(Integer, ForeignKey("shoes.id_shoe"))
    data_compra = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    clientes = relationship("Clientes", back_populates="cliente_shoes")
    shoes = relationship("Shoes", back_populates="cliente_shoes") 