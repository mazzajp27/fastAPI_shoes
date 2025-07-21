# app/schemas/clientes.py
from typing import Optional
from datetime import date
from .usuario import UsuarioBase

class VendedorBase(UsuarioBase):
    cnpj: Optional[str] = None
    descricao: Optional[str] = None
    documentos: Optional[str] = None
    status: Optional[str] = None
    data_cadastro: Optional[date] = None

class VendedorCreate(VendedorBase):
    pass

class VendedorUpdate(VendedorBase):
    pass

class VendedorResponse(VendedorBase):
    id: int
    class Config:
        from_attributes = True
