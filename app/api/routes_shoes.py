from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import shoes as crud_shoes
from app.schemas.shoes import ShoesCreate, ShoesUpdate, ShoesResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/shoes/", response_model=ShoesResponse)
def create_shoe(shoe: ShoesCreate, db: Session = Depends(get_db)):
    return crud_shoes.create_shoe(db, shoe)

@router.get("/shoes/", response_model=list[ShoesResponse])
def read_shoes(db: Session = Depends(get_db)):
    return crud_shoes.get_shoes(db)

@router.get("/shoes/{id_shoe}", response_model=ShoesResponse)
def read_shoe(id_shoe: int, db: Session = Depends(get_db)):
    db_shoe = crud_shoes.get_shoe(db, id_shoe)
    if db_shoe is None:
        raise HTTPException(status_code=404, detail="Shoe não encontrado")
    return db_shoe

@router.put("/shoes/{id_shoe}", response_model=ShoesResponse)
def update_shoe(id_shoe: int, shoe: ShoesUpdate, db: Session = Depends(get_db)):
    db_shoe = crud_shoes.update_shoe(db, id_shoe, shoe)
    if db_shoe is None:
        raise HTTPException(status_code=404, detail="Shoe não encontrado")
    return db_shoe