from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Para usar SQLite (arquivo local)
# banco = os.environ.get('BANCO')
# DATABASE_URL = f'sqlite:///./{banco}.db'

# Se depois quiser trocar para PostgreSQL, é só comentar o de cima e descomentar esse:
# Obtém as configurações do banco de dados através das variáveis de ambiente
usuario = os.getenv('USUARIO')
senha = os.getenv('SENHA')
banco = os.getenv('BANCO')
ambiente = os.getenv('AMBIENTE')
porta = os.getenv('PORTA')

DATABASE_URL = f'postgresql://{usuario}:{senha}@{ambiente}:{porta}/{banco}'

# Criação do engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

