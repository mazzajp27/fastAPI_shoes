# app/schemas/clientes.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClientesBase(BaseModel):
    nome: str
    telefone: str
    email : str
    senha : str
    endereco : Optional[str] = None
    genero : str
    data_nascimento : date


class ClientesCreate(ClientesBase):
    cpf: str

class ClientesUpdate(ClientesBase):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    endereco: Optional[str] = None
    genero: Optional[str] = None
    data_nascimento: Optional[date] = None


class ClientesResponse(ClientesBase):
    cpf: str

    class Config:
        orm_mode = True
