# app/schemas/clientes.py
from typing import Optional
from datetime import date
from .usuario import UsuarioBase

class VendedorBase(UsuarioBase):
    nome_loja : str
    cnpj: str
    descricao: Optional[str] = None

class VendedorCreate(VendedorBase):
    pass

class VendedorUpdate(VendedorBase):
    pass

class VendedorResponse(VendedorBase):
    id: int
    data_cadastro: date
    tipo: str
    nome_loja: str
    status: str
    cnpj: Optional[str] = None  
    descricao: Optional[str] = None
    class Config:
        from_attributes = True

class VendedorListResponse(UsuarioBase):
    id: int
    data_cadastro: date
    tipo: str
    status: str
    
    class Config:
        from_attributes = True