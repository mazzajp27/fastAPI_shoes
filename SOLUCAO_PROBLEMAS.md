# Solução de Problemas - FastAPI Shoes

## Problema: Erro `local_kw` na Autenticação

### ❌ Erro Original
```
TypeError: Session.__init__() got an unexpected keyword argument 'local_kw'
```

### ✅ Solução Aplicada
O problema estava na função `get_current_user` no arquivo `app/security/security.py`. A dependência estava sendo passada incorretamente.

**Antes (❌):**
```python
def get_current_user(db: Session = Depends(SessionLocal), token: str = Depends(oauth2_scheme)):
```

**Depois (✅):**
```python
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
```

### 🔧 Como Testar se Funcionou

1. **Reinicie o servidor**:
```bash
uvicorn app.main:app --reload
```

2. **Execute o teste**:
```bash
cd testes
python teste_simples.py
```

3. **Teste no Swagger**:
   - Acesse: `http://localhost:8000/docs`
   - Tente fazer login no endpoint `/api/token/`
   - Teste outros endpoints protegidos

## Outros Problemas Comuns

### 1. Erro de Importação Circular
**Sintoma**: `ImportError: cannot import name 'get_password_hash' from partially initialized module`

**Solução**: As funções de hash foram movidas para o módulo `security.py` principal.

### 2. Erro de Autenticação
**Sintoma**: `401 Unauthorized` ou `Could not validate credentials`

**Verificações**:
- ✅ Token está sendo enviado corretamente
- ✅ Token não expirou (30 minutos)
- ✅ Usuário existe no banco de dados
- ✅ Senha está correta

### 3. Erro de Banco de Dados
**Sintoma**: `IntegrityError` ou `DatabaseError`

**Soluções**:
- Verifique se o banco está acessível
- Execute as migrações: `alembic upgrade head`
- Verifique se as tabelas existem

### 4. Erro de CORS
**Sintoma**: Erro no frontend ao fazer requisições

**Solução**: O CORS já está configurado para permitir todas as origens em desenvolvimento.

## Como Debugar

### 1. Verificar Logs do Servidor
```bash
uvicorn app.main:app --reload --log-level debug
```

### 2. Testar Endpoints Individualmente
```bash
# Teste de login
curl -X POST "http://localhost:8000/api/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=seu_email&password=sua_senha"

# Teste de busca de usuários (com token)
curl -X GET "http://localhost:8000/api/usuarios/" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 3. Verificar Banco de Dados
```bash
# Se estiver usando SQLite
sqlite3 shoes.db
.tables
SELECT * FROM usuarios LIMIT 5;
```

## Checklist de Verificação

Antes de reportar um problema, verifique:

- [ ] Servidor está rodando (`uvicorn app.main:app --reload`)
- [ ] Banco de dados está acessível
- [ ] Migrações foram executadas
- [ ] Usuário existe no banco
- [ ] Credenciais estão corretas
- [ ] Token não expirou
- [ ] Headers estão corretos (Authorization: Bearer TOKEN)

## Comandos Úteis

```bash
# Iniciar servidor
uvicorn app.main:app --reload

# Executar migrações
alembic upgrade head

# Criar nova migração
alembic revision --autogenerate -m "descrição"

# Testar API
python testes/teste_simples.py

# Verificar dependências
pip list | grep fastapi
```

## Contato para Suporte

Se o problema persistir:
1. Verifique os logs completos
2. Teste com o script `teste_simples.py`
3. Verifique se todas as dependências estão instaladas
4. Confirme se o banco de dados está correto 