# app/schemas/clientes.py
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional
from datetime import date
from .usuario import UsuarioBase

class ClienteBase(UsuarioBase):
    preferencias: Optional[str] = None
    status: Optional[str] = None
    data_cadastro: Optional[date] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    class Config:
        from_attributes = True
