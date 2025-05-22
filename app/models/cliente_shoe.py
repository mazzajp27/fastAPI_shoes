from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ClienteShoe(Base):
    __tablename__ = "cliente_shoes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id_cliente"))
    shoe_id = Column(Integer, ForeignKey("shoes.id_shoe"))
    data_compra = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    cliente = relationship("Clientes", back_populates="compras")
    shoe = relationship("Shoes", back_populates="cliente_shoes") 