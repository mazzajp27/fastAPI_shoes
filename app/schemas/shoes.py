# app/schemas/shoes.py

from pydantic import BaseModel
from typing import Optional

class ShoesBase(BaseModel):
    nome: str
    preco: float
    descricao: Optional[str] = None
    quantidade: Optional[int] = None

class ShoesCreate(ShoesBase):
    pass

class ShoesUpdate(ShoesBase):
    pass

class ShoesResponse(ShoesBase):
    id_shoe: int

    class Config:
        orm_mode = True
