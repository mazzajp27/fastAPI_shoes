# app/models/user.py
from ast import Str
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_seller = Column(Boolean, default=False)
    is_buyer = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)

    
    # Relationships opcionais
    buyer = relationship("Buyer", back_populates="user", cascade="all, delete-orphan")
    seller = relationship("Seller", back_populates="user", cascade="all, delete-orphan")