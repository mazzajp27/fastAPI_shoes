# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from http import HTTPStatus
# from app.database import SessionLocal
# from app.crud import shoes as crud_shoes
# from app.models.shoes import Shoes
# # from app.models.cliente_shoe import ClienteShoe
# from app.models.user import User
# from app.security.security import get_current_seller, get_current_buyer
# from app.schemas.shoes import ShoesCreate, ShoesUpdate, ShoesResponse

# router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # --- Rotas públicas (clientes veem todos os tênis) ---
# @router.get("/shoes/", response_model=list[ShoesResponse])
# def read_shoes(db: Session = Depends(get_db)):
#     return crud_shoes.get_shoes(db)

# @router.get("/shoes/{id_shoe}", response_model=ShoesResponse)
# def read_shoe(id_shoe: int, db: Session = Depends(get_db)):
#     db_shoe = crud_shoes.get_shoe(db, id_shoe)
#     if db_shoe is None:
#         raise HTTPException(status_code=404, detail="Shoe não encontrado")
#     return db_shoe

# # --- Cliente compra um tênis ---
# # @router.post("/cliente-shoe/{id_shoe}", status_code=201)
# # def comprar_tenis(id_shoe: int, db: Session = Depends(get_db), current_cliente: Usuarios = Depends(get_current_cliente)):
# #     shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()
# #     if not shoe:
# #         raise HTTPException(status_code=404, detail="Tênis não encontrado")
# #     relacao = ClienteShoe(cliente_id=current_cliente.id, shoe_id=id_shoe)
# #     db.add(relacao)
# #     db.commit()
# #     db.refresh(relacao)
# #     return {"message": "Compra realizada com sucesso!", "shoe_id": id_shoe}

# # --- Vendedor: adicionar tênis ---
# # @router.post("/shoes/",status_code=HTTPStatus.CREATED,  response_model=ShoesResponse)
# # def create_shoe(shoe: ShoesCreate, db: Session = Depends(get_db), current_vendedor: User = Depends(get_current_vendedor)):
# #     return crud_shoes.create_shoe(db, shoe, vendedor_id=current_vendedor.id)

# # --- Vendedor: listar só seus tênis ---
# # @router.get("/shoes/me", response_model=list[ShoesResponse])
# # def read_my_shoes(db: Session = Depends(get_db), current_vendedor: User = Depends(get_current_vendedor)):
# #     return db.query(Shoes).filter(Shoes.vendedor_id == current_vendedor.id).all()

# # --- Vendedor: editar/deletar só seus tênis ---
# # @router.put("/shoes/{id_shoe}", response_model=ShoesResponse)
# # def update_shoe(id_shoe: int, shoe: ShoesUpdate, db: Session = Depends(get_db), current_vendedor: User = Depends(get_current_vendedor)):
# #     db_shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe, Shoes.vendedor_id == current_vendedor.id).first()
# #     if db_shoe is None:
# #         raise HTTPException(status_code=404, detail="Você só pode editar seus próprios tênis")
# #     for key, value in shoe.dict(exclude_unset=True).items():
# #         setattr(db_shoe, key, value)
# #     db.commit()
# #     db.refresh(db_shoe)
# #     return db_shoe

# # @router.delete("/shoes/{id_shoe}", response_model=ShoesResponse)
# # def delete_shoe(id_shoe: int, db: Session = Depends(get_db), current_vendedor: User = Depends(get_current_vendedor)):
# #     db_shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe, Shoes.vendedor_id == current_vendedor.id).first()
# #     if db_shoe is None:
# #         raise HTTPException(status_code=404, detail="Você só pode deletar seus próprios tênis")
# #     db.delete(db_shoe)
# #     db.commit()
# #     return db_shoe

# # --- Admin: editar/deletar/ver todos os tênis ---
# # @router.put("/admin/shoes/{id_shoe}", response_model=ShoesResponse)
# # def admin_update_shoe(id_shoe: int, shoe: ShoesUpdate, db: Session = Depends(get_db), current_admin: Usuarios = Depends(get_current_admin)):
# #     db_shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()
# #     if db_shoe is None:
# #         raise HTTPException(status_code=404, detail="Tênis não encontrado")
# #     for key, value in shoe.dict(exclude_unset=True).items():
# #         setattr(db_shoe, key, value)
# #     db.commit()
# #     db.refresh(db_shoe)
# #     return db_shoe

# # @router.delete("/admin/shoes/{id_shoe}", response_model=ShoesResponse)
# # def admin_delete_shoe(id_shoe: int, db: Session = Depends(get_db), current_admin: Usuarios = Depends(get_current_admin)):
# #     db_shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()
# #     if db_shoe is None:
# #         raise HTTPException(status_code=404, detail="Tênis não encontrado")
# #     db.delete(db_shoe)
# #     db.commit()
# #     return db_shoe

# # --- Admin: ver relação de um tênis com cliente/vendedor ---
# # @router.get("/admin/shoes/{id_shoe}/relacoes", response_model=dict)
# # def relacoes_tenis(id_shoe: int, db: Session = Depends(get_db), current_admin: Usuarios = Depends(get_current_admin)):
# #     shoe = db.query(Shoes).filter(Shoes.id_shoe == id_shoe).first()
# #     if not shoe:
# #         raise HTTPException(status_code=404, detail="Tênis não encontrado")
# #     vendedor = db.query(Usuarios).filter(Usuarios.id == shoe.vendedor_id).first()
# #     clientes = db.query(ClienteShoe).filter(ClienteShoe.shoe_id == id_shoe).all()
# #     return {
# #         "tenis": shoe.nome,
# #         "vendedor": vendedor.nome if vendedor else None,
# #         "clientes": [db.query(User).filter(User.user_id == c.cliente_id).first().nome for c in clientes]
# #     }