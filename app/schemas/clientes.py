# app/schemas/clientes.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ClientesBase(BaseModel):
    cpf: str
    nome: str
    telefone: str
    email : EmailStr
    senha : str
    genero : str
    data_nascimento : date

class ClientesCreate(ClientesBase):
    pass

class ClientesUpdate(BaseModel):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    genero: Optional[str] = None
    data_nascimento: Optional[date] = None

class ClientesResponse(ClientesBase):
    id_cliente: int

    class Config:
        from_attributes = True

class ClienteLogin(BaseModel):
    email: EmailStr
    senha: str

class ClienteLoginResponse(BaseModel):
    token: str
    user: ClientesResponse