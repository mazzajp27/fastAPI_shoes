# # app/schemas/shoes.py
# from pydantic import BaseModel
# from typing import Optional


# class ShoesBase(BaseModel):
#     name: str
#     price: float
#     description: Optional[str] = None
#     quantity: int = None
#     image: Optional[str] = None
#     brand: str
#     model: str
#     size: int
#     color: str


# class ShoesCreate(ShoesBase):
#     pass
 

# class ShoesUpdate(ShoesBase):
#     name: Optional[str] = None
#     price: Optional[float] = None
#     description: Optional[str] = None
#     quantity: Optional[int] = None
#     image: Optional[str] = None
#     brand: Optional[str] = None
#     model: Optional[str] = None
#     size: Optional[int] = None
#     color: Optional[str] = None


# class ShoesResponse(ShoesBase):
#     shoe_id: int


#     class Config:
#         from_attributes = True