# app/schemas/clientes.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClientesBase(BaseModel):
    nome: str
    telefone: str
    email = str
    senha = str
    endereco = Optional[str] = None
    genero = str
    data_nascimento = date


class ClientesCreate(ClientesBase):
    pass

class ClientesUpdate(ClientesBase):
    pass

class ClientesResponse(ClientesBase):
    CPF: str

    class Config:
        orm_mode = True
