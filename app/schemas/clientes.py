# app/schemas/clientes.py
from typing import Optional
from datetime import date
from .usuario import UsuarioBase

class ClienteBase(UsuarioBase):
    preferencias: Optional[str] = None
    
class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    data_cadastro: date
    tipo: str
    status: str
    class Config:
        from_attributes = True

class ClienteListResponse(UsuarioBase):
    id: int
    data_cadastro: date
    tipo: str
    status: str
    
    class Config:
        from_attributes = True
