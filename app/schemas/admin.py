# app/schemas/clientes.py
from typing import Optional
from datetime import date
from .usuario import UsuarioBase

class AdminBase(UsuarioBase):
    nivel_acesso: str
class AdminCreate(AdminBase):
    pass

class AdminUpdate(AdminBase):
    pass

class AdminResponse(AdminBase):
    id: int
    data_cadastro: date
    tipo: str
    status: str

    class Config:
        from_attributes = True

class AdminListResponse(UsuarioBase):
    id: int
    data_cadastro: date
    tipo: str
    status: str
    
    class Config:
        from_attributes = True