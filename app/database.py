from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Para usar SQLite (arquivo local)
DATABASE_URL = 'sqlite:///./shoes.db'

# Se depois quiser trocar para PostgreSQL, é só comentar o de cima e descomentar esse:
# DATABASE_URL = 'postgresql://postgres:Apex123.@localhost:5432/shoes'

# Criação do engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
