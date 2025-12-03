# app/schemas/usuario.py
import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class UserBase(BaseModel):
    full_name: str
    cpf: str
    email: EmailStr
    birthdate: date
    gender: str
    is_active: bool = True
    is_superuser: bool = False
    is_seller: bool = True
    is_buyer: bool = True
    

class UserCreate(UserBase):
    full_name: str
    cpf: str
    email: EmailStr
    birthdate: date
    gender: str
    password: str
    is_active: bool
    is_superuser: bool 
    is_seller: bool 
    is_buyer: bool 


class UserCreatePublic(UserBase):
    full_name: str
    cpf: str
    email: EmailStr
    birthdate: date
    gender: str
    password: str
    is_seller: bool
    is_buyer: bool
    password: str


class UserUpdate(UserBase):
    full_name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_seller: Optional[bool] = None
    is_buyer: Optional[bool] = None


class UserDisplay(UserBase):
    user_id: int
    created_at: datetime


    class Config:
        from_attributes = True
