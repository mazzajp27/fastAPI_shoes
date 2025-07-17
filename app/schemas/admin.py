# app/schemas/clientes.py
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional
from datetime import date
from .usuario import UsuarioBase

class AdminBase(UsuarioBase):
    nivel_acesso: str
    status: Optional[str] = None
    data_cadastro: Optional[date] = None

class AdminCreate(AdminBase):
    pass

class AdminUpdate(AdminBase):
    pass

class AdminResponse(AdminBase):
    id: int
    class Config:
        from_attributes = True