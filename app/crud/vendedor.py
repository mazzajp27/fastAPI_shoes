from sqlalchemy.orm import Session
from app.models.vendedor import Vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate
from app.security.security import get_password_hash, verify_password
from app.models.usuario import Usuarios

def create_vendedor(db: Session, vendedor: VendedorCreate):
    db_vendedor = Vendedor(**vendedor.dict())
    db_vendedor.tipo = "vendedor"  
    db_vendedor.status = "ativo"
    db_vendedor.senha = get_password_hash(db_vendedor.senha)
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def get_vendedores(db: Session):
    return db.query(Usuarios).filter(Usuarios.tipo == "vendedor").all()

def get_vendedor(db: Session, id: int):
    """Busca vendedor por ID, funcionando com herança de tabelas"""
    # Primeiro tenta buscar na tabela vendedor
    vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    
    # Se não encontrar, busca na tabela usuarios e verifica se é vendedor
    if not vendedor:
        usuario = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "vendedor").first()
        if usuario:
            # Se encontrou um usuário do tipo vendedor, retorna ele
            return usuario
    
    return vendedor

def update_vendedor(db: Session, id: int, vendedor: VendedorUpdate):
    """Atualiza vendedor por ID, funcionando com herança de tabelas"""
    # Primeiro tenta buscar na tabela vendedor
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    
    # Se não encontrar, busca na tabela usuarios
    if not db_vendedor:
        db_vendedor = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "vendedor").first()
    
    if db_vendedor:
        update_data = vendedor.dict(exclude_unset=True)
        
        # Se a senha foi fornecida, fazer hash dela
        if "senha" in update_data:
            update_data["senha"] = get_password_hash(update_data["senha"])
        
        for key, value in update_data.items():
            setattr(db_vendedor, key, value)
        db.commit()
        db.refresh(db_vendedor)
    return db_vendedor

def delete_vendedor(db: Session, id: int):
    """Deleta vendedor por ID, funcionando com herança de tabelas"""
    # Primeiro tenta buscar na tabela vendedor
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    
    # Se não encontrar, busca na tabela usuarios
    if not db_vendedor:
        db_vendedor = db.query(Usuarios).filter(Usuarios.id == id, Usuarios.tipo == "vendedor").first()
    
    if db_vendedor is None:
        return None
    
    # Soft delete - apenas marcar como inativo
    db_vendedor.status = "inativo"
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def login_vendedor(db: Session, email: str, senha: str):
    """
    Função para login de vendedor com verificação de senha hash
    """
    vendedor = db.query(Vendedor).filter(Vendedor.email == email).first()
    if not vendedor:
        return None
    
    # Verificar se o vendedor está ativo
    if vendedor.status != "ativo":
        return None
    
    # Verificar senha usando hash
    if not verify_password(senha, vendedor.senha):
        return None
    
    return vendedor

def get_vendedor_by_user_id(db: Session, user_id: int):
    """Busca vendedor pelo ID do usuário autenticado"""
    # Primeiro tenta buscar diretamente na tabela vendedor
    vendedor = db.query(Vendedor).filter(Vendedor.id == user_id).first()
    
    # Se não encontrar, busca na tabela usuarios e verifica se é vendedor
    if not vendedor:
        usuario = db.query(Usuarios).filter(Usuarios.id == user_id).first()
        if usuario and usuario.tipo == "vendedor":
            # Se é um vendedor, retorna o objeto como vendedor
            return usuario
    
    return vendedor

def get_vendedor_by_email(db: Session, email: str):
    """Busca vendedor pelo email"""
    return db.query(Vendedor).filter(Vendedor.email == email).first()

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

def check_cnpj_exists(db: Session, cnpj: str, exclude_id: int = None):
    """Verifica se um CNPJ já existe, opcionalmente excluindo um ID específico"""
    query = db.query(Vendedor).filter(Vendedor.cnpj == cnpj)
    if exclude_id:
        query = query.filter(Vendedor.id != exclude_id)
    return query.first() is not None 