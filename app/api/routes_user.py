from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserUpdate, UserDisplay
from app.security.security import get_current_user, get_password_hash
from sqlalchemy.exc import IntegrityError
from app.models.user import User


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/", response_model=list[UserDisplay])
def read_users(db: Session = Depends(get_db)): 
    return crud_user.get_user(db)


@router.get("/users/{id_user}", response_model=UserDisplay)
def read_user(id_user: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_id(db, id_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserDisplay)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = crud_user.create_user(db, user)
    return new_user


@router.put("/users/{id_user}", response_model=UserDisplay)
def update_user(id_user: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.update_user(db, id_user, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/alter-status/{user_id}", response_model=UserDisplay)
def alter_status_user(user_id: int,db: Session = Depends(get_db)):
    """Delete user by user_id"""
    return crud_user.alter_status_user(db, user_id)

@router.delete("/users/{id_user}", response_model=UserDisplay )
def delete_user(id_user:int, db: Session = Depends(get_db)):
    db_user = crud_user.delete_user(db, id_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user 