# app/main.py
from fastapi import FastAPI
from app.api import routes_shoes
from app.api import routes_clientes
from app.api import routes_cliente_shoe
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Libera acesso ao frontend (por exemplo: localhost ou outro)
origins = [
     "http://127.0.0.1:5500",  # Se estiver rodando o HTML local com Live Server (VS Code)
     "http://localhost:5500",  # Ou outra porta
     "http://127.0.0.1:8000",  # Se for consumir do Swagger
 ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique origens: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos: GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Permite todos os headers
)

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

# Incluir as rotas
app.include_router(routes_shoes.router, prefix="/api", tags=["shoes"])
app.include_router(routes_clientes.router, prefix="/api", tags=["clientes"])
app.include_router(routes_cliente_shoe.router, prefix="/api", tags=["cliente-shoe"])