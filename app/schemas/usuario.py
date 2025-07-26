# app/schemas/usuario.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UsuarioBase(BaseModel):
    cpf: str
    nome: str
    telefone: str
    endereco:str
    email: EmailStr
    senha: str
    genero: str
    data_nascimento: date

class UsuarioCreate(UsuarioBase):
    cpf: str
    nome: str
    telefone: str
    endereco: str
    email: EmailStr
    senha: str
    genero: str
    data_nascimento: date
    tipo: str

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
    data_cadastro: date
    tipo: str
    status: str
    
    class Config:
        from_attributes = True
