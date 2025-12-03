# app/models/buyer.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Buyer(Base):
    __tablename__ = "buyer"

    buyer_id = Column(Integer, primary_key=True, autoincrement=True)
    preferences = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)

    user = relationship("User", back_populates="buyer")
    
    # buyer_shoes = relationship("BuyerShoe", back_populates="buyer")