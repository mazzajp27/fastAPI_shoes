from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClienteShoeBase(BaseModel):
    cliente_id: int
    shoe_id: int

class ClienteShoeCreate(ClienteShoeBase):
    pass

class ClienteShoeResponse(ClienteShoeBase):
    id: int
    data_compra: datetime

    class Config:
        from_attributes = True 