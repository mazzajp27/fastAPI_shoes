# app/crud/clientes.py

from sqlalchemy.orm import Session
from app.models.clientes import Clientes
from app.schemas.clientes import ClienteCreate, ClienteUpdate
from app.security.security import get_password_hash, verify_password
from app.models.usuario import Usuarios

def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Clientes(**cliente.dict())
    db_cliente.tipo = "clientes"
    db_cliente.status = "ativo"
    db_cliente.senha = get_password_hash(db_cliente.senha)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_clientes(db: Session):
    return db.query(Usuarios).filter(Usuarios.tipo == "clientes").all()

def get_cliente(db: Session, id: int):
    """Busca cliente por ID, funcionando com herança de tabelas"""
    # Primeiro tenta buscar na tabela clientes
    cliente = db.query(Clientes).filter(Clientes.id == id).first()
    
    # Se não encontrar, busca na tabela usuarios e verifica se é cliente
    if not cliente:
        usuario = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "clientes").first()
        if usuario:
            # Se encontrou um usuário do tipo cliente, retorna ele
            return usuario
    
    return cliente

def update_cliente(db: Session, id: int, cliente: ClienteUpdate):
    """Atualiza cliente por ID, funcionando com herança de tabelas"""
    # Primeiro tenta buscar na tabela clientes
    db_cliente = db.query(Clientes).filter(Clientes.id == id).first()
    
    # Se não encontrar, busca na tabela usuarios
    if not db_cliente:
        db_cliente = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "clientes").first()
    
    if db_cliente:
        update_data = cliente.dict(exclude_unset=True)
        
        # Se a senha foi fornecida, fazer hash dela
        if "senha" in update_data:
            update_data["senha"] = get_password_hash(update_data["senha"])
        
        for key, value in update_data.items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, id: int):
    """Deleta cliente por ID, funcionando com herança de tabelas"""
    # Primeiro tenta buscar na tabela clientes
    db_cliente = db.query(Clientes).filter(Clientes.id == id).first()
    
    # Se não encontrar, busca na tabela usuarios
    if not db_cliente:
        db_cliente = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "clientes").first()
    
    if db_cliente is None:
        return None
    
    # Soft delete - apenas marcar como inativo
    db_cliente.status = "inativo"
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def login_cliente(db: Session, email: str, senha: str):
    """
    Função para login de cliente com verificação de senha hash
    """
    cliente = db.query(Clientes).filter(Clientes.email == email).first()
    if not cliente:
        return None
    
    # Verificar se o cliente está ativo
    if cliente.status != "ativo":
        return None
    
    # Verificar senha usando hash
    if not verify_password(senha, cliente.senha):
        return None
    
    return cliente

def get_cliente_by_user_id(db: Session, user_id: int):
    """Busca cliente pelo ID do usuário autenticado"""
    # Primeiro tenta buscar diretamente na tabela clientes
    cliente = db.query(Clientes).filter(Clientes.id == user_id).first()
    
    # Se não encontrar, busca na tabela usuarios e verifica se é cliente
    if not cliente:
        usuario = db.query(Usuarios).filter(Usuarios.id == user_id).first()
        if usuario and usuario.tipo == "clientes":
            # Se é um cliente, retorna o objeto como cliente
            return usuario
    
    return cliente

def get_cliente_by_email(db: Session, email: str):
    """Busca cliente pelo email"""
    return db.query(Clientes).filter(Clientes.email == email).first()

def check_email_exists(db: Session, email: str, exclude_id: int = None):
    """Verifica se um email já existe, opcionalmente excluindo um ID específico"""
    query = db.query(Usuarios).filter(Usuarios.email == email)
    if exclude_id:
        query = query.filter(Usuarios.id != exclude_id)
    return query.first() is not None

def check_cpf_exists(db: Session, cpf: str, exclude_id: int = None):
    """Verifica se um CPF já existe, opcionalmente excluindo um ID específico"""
    query = db.query(Usuarios).filter(Usuarios.cpf == cpf)
    if exclude_id:
        query = query.filter(Usuarios.id != exclude_id)
    return query.first() is not None