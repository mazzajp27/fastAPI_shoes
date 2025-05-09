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
    endereco : Optional[str] = None
    genero : str
    data_nascimento : date


class ClientesCreate(ClientesBase):
    pass

class ClientesUpdate(ClientesBase):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    endereco: Optional[str] = None
    genero: Optional[str] = None
    data_nascimento: Optional[date] = None


class ClientesResponse(ClientesBase):
    id_cliente: int

    class Config:
        orm_mode = True
