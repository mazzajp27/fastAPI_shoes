# app/schemas/clientes.py
from typing import Optional
from datetime import date
from .usuario import UsuarioBase

class VendedorBase(UsuarioBase):
    cnpj: str
    descricao: Optional[str] = None
    documentos: str

class VendedorCreate(VendedorBase):
    pass

class VendedorUpdate(VendedorBase):
    pass

class VendedorResponse(VendedorBase):
    id: int
    data_cadastro: date
    tipo: str
    status: str
    class Config:
        from_attributes = True
