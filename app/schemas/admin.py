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
    data_cadastro: Optional[date] = None
    tipo: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True