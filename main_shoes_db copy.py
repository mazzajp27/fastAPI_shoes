from typing import List, Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import routes

app = FastAPI()

app.include_router(routes.router)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Durante o desenvolvimento, aceita tudo
#     allow_credentials=True,
#     allow_methods=["*"],  # Permite todos os métodos (POST, GET, DELETE etc)
#     allow_headers=["*"],  # Permite todos os headers
# )


models.Base.metadata.create_all(bind=engine) #Cria todas as tabelas e colunas no Postgre


# # class ShoesModel(BaseModel):
# #     # id_shoe = int
# #     nome: str
# #     preco: float
# #     descricao: Optional[str] = None
# #     quantidade: Optional[int] = None
    
    
def get_db():# Conexão com a base de dados
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   

db_dependency = Annotated[Session, Depends(get_db)]   

       

# @app.post("/insert",status_code=status.HTTP_201_CREATED,  response_model = List[models.Shoes1])
# async def post_shoes(db: db_dependency):
#     shoes = models.Shoes(nome = shoes.nome, preco = shoes.preco, descricao = shoes.descricao, quantidade = shoes.quantidade)
    
#     db.add(shoes)
#     db.commit()
#     db.refresh(shoes)
#     return {
#             "mensagem": "Produto cadastrado com sucesso",
#             "dados": shoes
#         }


# @app.get("/qtd_shoes",status_code=status.HTTP_200_OK)
# async def get_shoes(db: db_dependency):
#     shoes_list = db.query(models.Shoes).all()
#     # shoe_id = shoes_list.id_shoe
#     # print(shoe_id)
#     return shoes_list
#     # return {"Tudo":shoes_list}



# @app.get("/shoes/{shoes_id}", status_code=status.HTTP_200_OK)
# async def get_especific_shoe(shoes_id: int, db: db_dependency):
#     shoes = db.query(models.Shoes).filter(models.Shoes.id_shoe == shoes_id).first()
    
#     if shoes is None:
#         raise HTTPException(status_code=404, detail="Tênis não encontrado")
    
#     return shoes



# @app.put("/shoes/{shoes_id}")
# async def update_shoe(shoes_id: int,db:db_dependency):
#     shoes = db.query(models.Shoes).filter(models.Shoes.id_shoe == shoes_id).first()
#     if shoes is None:
#         raise HTTPException(status_code=404, detail=f"The id:{id} does not exist")
#     # shoes.update(shoes.dict(), synchronize_session=False)
#     shoes.nome = updated_shoes.nome
#     shoes.descricao = updated_shoes.descricao
#     shoes.preco = updated_shoes.preco
#     shoes.quantidade = updated_shoes.quantidade
#     db.commit()
#     db.refresh(shoes)

#     return  shoes

# @app.delete("/shoes_del/{shoes_id}")
# async def delete_shoe(shoes_id:int,db:db_dependency):
#     shoes = db.query(models.Shoes).filter(models.Shoes.id_shoe == shoes_id).first()
#     if shoes is None:
#         raise HTTPException(status_code=404, detail=f"The id:{id} does not exist")
#     # shoes.nome = delete_shoes.nome
#     # shoes.descricao = delete_shoes.descricao
#     # shoes.preco = delete_shoes.preco
#     # shoes.quantidade = delete_shoes.quantidade
#     db.delete(shoes)
#     db.commit()

#     return  shoes