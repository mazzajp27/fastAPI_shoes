# app/schemas/buyer.py
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, model_validator


class BuyerBase(BaseModel):
    preferences: Optional[str] = None


class BuyerCreate(BuyerBase):
    user_id: Optional[int] = None


class BuyerCreateWithUser(BaseModel):
    full_name: str
    cpf: str
    email: EmailStr
    birthdate: date
    gender: str
    password: str
    preferences: Optional[str] = None


class BuyerUpdate(BuyerBase):
    pass


# Schema para User (para usar no BuyerDisplay)
class UserInBuyer(BaseModel):
    full_name: str
    cpf: str
    email: EmailStr
    birthdate: date
    gender: str
    password: str


    class Config:
        from_attributes = True


class BuyerDisplay(BaseModel):
    buyer_id: int
    user_id: int
    preferences: Optional[str] = None
    user: UserInBuyer
    
    class Config:
        from_attributes = True