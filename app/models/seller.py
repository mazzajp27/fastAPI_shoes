# app/models/seller.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Seller(Base):
    __tablename__ = "seller"

    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String,unique=True, nullable=True)
    cnpj = Column(String, unique=True, index=True, nullable=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    
    user = relationship("User", back_populates="seller")
    
    # shoes = relationship("Shoes", back_populates="seller")