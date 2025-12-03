# app/schemas/clientes.py
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr
from datetime import datetime


class SellerBase(BaseModel):
    store_name : Optional[str] = None
    cnpj: Optional[str] = None
    description: Optional[str] = None


class SellerCreate(SellerBase):
    store_name: str
    cnpj: str
    description: Optional[str] = None
    user_id: int


class SellerCreateWithUser(BaseModel):
    """Complete schema for creation - includes User and Seller fields"""
    # Campos do User
    full_name: str
    cpf: str
    email: EmailStr
    birthdate: date
    gender: str
    password: str
    # Campos do Seller
    store_name: str
    cnpj: str
    description: Optional[str] = None


class SellerUpdate(SellerBase):
    store_name: Optional[str] = None
    cnpj: Optional[str] = None
    description: Optional[str] = None
    

class UserInSeller(BaseModel):
    full_name: str
    cpf: str
    email: EmailStr
    birthdate: date
    gender: str
    password: str


    class Config:
        from_attributes = True




class SellerDisplay(SellerBase):
    seller_id: int
    user_id: int
    store_name: Optional[str] = None
    cnpj: Optional[str] = None
    description: Optional[str] = None
    user: UserInSeller


    class Config:
        from_attributes = True
