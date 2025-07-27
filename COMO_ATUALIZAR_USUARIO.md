# Como Atualizar um Usuário

## Visão Geral

O sistema permite atualizar dados de usuários através da API REST. A atualização é feita através do endpoint `PUT /api/usuarios/{id}`.

## Pré-requisitos

1. **Autenticação**: Você precisa estar logado e ter um token de acesso válido
2. **Autorização**: 
   - Você só pode atualizar seu próprio perfil
   - Administradores podem atualizar qualquer usuário
3. **Servidor rodando**: A API deve estar em execução

## Passos para Atualizar um Usuário

### 1. Iniciar o Servidor

```bash
cd fastAPI_shoes
uvicorn app.main:app --reload
```

### 2. Fazer Login para Obter Token

**Endpoint**: `POST /api/token`

**Dados necessários**:
```json
{
  "username": "seu_email@exemplo.com",
  "password": "sua_senha"
}
```

**Exemplo com curl**:
```bash
curl -X POST "http://localhost:8000/api/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=seu_email@exemplo.com&password=sua_senha"
```

**Resposta**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 3. Atualizar o Usuário

**Endpoint**: `PUT /api/usuarios/{id}`

**Headers necessários**:
```
Authorization: Bearer {seu_token}
Content-Type: application/json
```

**Dados que podem ser atualizados**:
```json
{
  "nome": "Novo Nome",
  "telefone": "(11) 99999-8888",
  "endereco": "Nova Rua, 123",
  "email": "novo@email.com",
  "senha": "nova_senha",
  "genero": "M",
  "data_nascimento": "1990-01-01",
  "tipo": "cliente"
}
```

**Exemplo com curl**:
```bash
curl -X PUT "http://localhost:8000/api/usuarios/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "telefone": "(11) 99999-8888",
    "endereco": "Rua das Flores, 123"
  }'
```

## Campos Opcionais

Você pode enviar apenas os campos que deseja atualizar. Os campos não enviados permanecerão inalterados.

**Exemplo - atualizar apenas o telefone**:
```json
{
  "telefone": "(11) 88888-7777"
}
```

## Tratamento de Senha

Se você incluir o campo `senha` na atualização, ela será automaticamente criptografada antes de ser salva no banco de dados.

## Validações

- **Email único**: Se você alterar o email, ele deve ser único no sistema
- **CPF único**: Se você alterar o CPF, ele deve ser único no sistema
- **Telefone único**: Se você alterar o telefone, ele deve ser único no sistema
- **Formato de data**: A data de nascimento deve estar no formato YYYY-MM-DD

## Códigos de Resposta

- **200**: Usuário atualizado com sucesso
- **400**: Dados inválidos ou já existentes
- **401**: Token inválido ou expirado
- **403**: Usuário não autorizado (tentando atualizar outro usuário)
- **404**: Usuário não encontrado

## Exemplo Completo com Python

```python
import requests

# 1. Login
login_data = {
    "username": "usuario@exemplo.com",
    "password": "senha123"
}

response = requests.post("http://localhost:8000/api/token", data=login_data)
token = response.json()["access_token"]

# 2. Atualizar usuário
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

update_data = {
    "nome": "Novo Nome",
    "telefone": "(11) 99999-8888"
}

response = requests.put(
    "http://localhost:8000/api/usuarios/1",
    json=update_data,
    headers=headers
)

if response.status_code == 200:
    print("Usuário atualizado com sucesso!")
    print(response.json())
else:
    print(f"Erro: {response.text}")
```

## Teste Automatizado

Execute o script de teste incluído:

```bash
cd testes
python teste_atualizacao_usuario.py
```

**Lembre-se de ajustar as credenciais no script antes de executar!**

## Swagger UI

Você também pode testar a API através da interface Swagger:

1. Acesse: `http://localhost:8000/docs`
2. Faça login primeiro usando o endpoint `/api/token`
3. Use o endpoint `PUT /api/usuarios/{id}` para atualizar usuários

## Observações Importantes

1. **Segurança**: Sempre use HTTPS em produção
2. **Tokens**: Os tokens expiram em 30 minutos
3. **Backup**: Faça backup dos dados antes de atualizações em massa
4. **Logs**: Monitore os logs para detectar tentativas de acesso não autorizado 