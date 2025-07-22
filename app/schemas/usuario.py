# app/schemas/usuario.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UsuarioBase(BaseModel):
    cpf: str
    nome: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    email: EmailStr
    senha: str
    genero: Optional[str] = None
    data_nascimento: Optional[date] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    genero: Optional[str] = None
    data_nascimento: Optional[date] = None
    tipo: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    data_cadastro: Optional[date] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    class Config:
        from_attributes = True
