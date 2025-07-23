from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import vendedor as crud_vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate, VendedorResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/vendedores/", status_code=HTTPStatus.CREATED, response_model=VendedorResponse)
def create_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    novo_vendedor = crud_vendedor.create_vendedor(db, vendedor)
    return novo_vendedor

@router.get("/vendedores/", response_model=list[VendedorResponse])
def read_vendedores(db: Session = Depends(get_db)):
    return crud_vendedor.get_vendedores(db)

@router.get("/vendedores/{id}", response_model=VendedorResponse)
def read_vendedor(id: int, db: Session = Depends(get_db)):
    db_vendedor = crud_vendedor.get_vendedor(db, id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return db_vendedor

@router.put("/vendedores/{id}", response_model=VendedorResponse)
def update_vendedor(id: int, vendedor: VendedorUpdate, db: Session = Depends(get_db)):
    db_vendedor = crud_vendedor.update_vendedor(db, id, vendedor)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return db_vendedor

@router.delete("/vendedores/{id}", response_model=VendedorResponse)
def delete_vendedor(id: int, db: Session = Depends(get_db)):
    db_vendedor = crud_vendedor.delete_vendedor(db, id)
    if db_vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return db_vendedor 