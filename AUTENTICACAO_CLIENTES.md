# Guia de Autenticação de Clientes

## Visão Geral

Este documento explica como usar o sistema de autenticação de clientes implementado no projeto FastAPI de calçados.

## Funcionalidades Implementadas

### ✅ Sistema Completo de Autenticação
- **JWT Tokens** com access e refresh tokens
- **Validação de permissões** por tipo de usuário
- **Verificação de status** (ativo/inativo)
- **Hash seguro de senhas** usando pwdlib
- **Refresh automático** de tokens
- **Soft delete** para clientes

## Endpoints Disponíveis

### 1. Registro de Cliente
```http
POST /api/clientes/register
```

**Body:**
```json
{
  "cpf": "123.456.789-00",
  "nome": "João Silva",
  "telefone": "(11) 99999-9999",
  "endereco": "Rua das Flores, 123",
  "email": "joao@email.com",
  "senha": "senha123",
  "genero": "M",
  "data_nascimento": "1990-01-01",
  "preferencias": "Tênis esportivo"
}
```

**Resposta:**
```json
{
  "id": 1,
  "cpf": "123.456.789-00",
  "nome": "João Silva",
  "telefone": "(11) 99999-9999",
  "endereco": "Rua das Flores, 123",
  "email": "joao@email.com",
  "genero": "M",
  "data_nascimento": "1990-01-01",
  "tipo": "clientes",
  "status": "ativo",
  "data_cadastro": "2024-01-01",
  "preferencias": "Tênis esportivo"
}
```

### 2. Login
```http
POST /api/token/
```

**Body (form-data):**
```
username: joao@email.com
password: senha123
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 1800,
  "user_id": 1,
  "user_email": "joao@email.com",
  "user_tipo": "clientes"
}
```

### 3. Refresh Token
```http
POST /api/token/refresh
```

**Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

### 4. Informações do Usuário Atual
```http
GET /api/me
Authorization: Bearer <access_token>
```

**Resposta:**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "tipo": "clientes",
  "status": "ativo"
}
```

### 5. Logout
```http
POST /api/logout
Authorization: Bearer <access_token>
```

**Resposta:**
```json
{
  "message": "Logout realizado com sucesso. Invalide os tokens no cliente."
}
```

## Endpoints Protegidos para Clientes

### Perfil do Cliente
```http
GET /api/clientes/me
Authorization: Bearer <access_token>
```

### Atualizar Perfil
```http
PUT /api/clientes/me
Authorization: Bearer <access_token>
```

### Deletar Conta (Soft Delete)
```http
DELETE /api/clientes/me
Authorization: Bearer <access_token>
```

## Como Usar no Frontend

### 1. Registro
```javascript
const registerCliente = async (clienteData) => {
  const response = await fetch('/api/clientes/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(clienteData)
  });
  return response.json();
};
```

### 2. Login
```javascript
const login = async (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await fetch('/api/token/', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  
  // Salvar tokens no localStorage
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  localStorage.setItem('user_info', JSON.stringify({
    id: data.user_id,
    email: data.user_email,
    tipo: data.user_tipo
  }));
  
  return data;
};
```

### 3. Requisições Autenticadas
```javascript
const getClienteProfile = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('/api/clientes/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.status === 401) {
    // Token expirado, tentar refresh
    await refreshToken();
    return getClienteProfile(); // Tentar novamente
  }
  
  return response.json();
};
```

### 4. Refresh Token Automático
```javascript
const refreshToken = async () => {
  const refresh_token = localStorage.getItem('refresh_token');
  
  const response = await fetch('/api/token/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data;
  } else {
    // Refresh token expirado, fazer logout
    logout();
    throw new Error('Sessão expirada');
  }
};
```

### 5. Logout
```javascript
const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_info');
  // Redirecionar para página de login
  window.location.href = '/login';
};
```

## Validações Implementadas

### ✅ Validações de Registro
- Email único
- CPF único
- Telefone único
- Senha com hash seguro
- Status automático como "ativo"

### ✅ Validações de Login
- Verificação de email e senha
- Verificação de status ativo
- Geração de tokens JWT seguros

### ✅ Validações de Acesso
- Verificação de token válido
- Verificação de tipo de usuário (clientes/admin/vendedor)
- Verificação de status ativo
- Refresh automático de tokens

## Segurança

### 🔒 Medidas Implementadas
- **Hash de senhas** usando pwdlib (recomendado)
- **JWT tokens** com expiração
- **Refresh tokens** para renovação automática
- **Validação de status** de usuário
- **Soft delete** para preservar dados
- **Verificação de permissões** por tipo

### ⚠️ Configurações de Produção
1. **Alterar SECRET_KEY** em `app/security/security.py`
2. **Configurar HTTPS** em produção
3. **Implementar rate limiting**
4. **Configurar CORS** adequadamente
5. **Usar variáveis de ambiente** para configurações sensíveis

## Exemplo de Uso Completo

```javascript
// 1. Registrar cliente
const novoCliente = await registerCliente({
  cpf: "123.456.789-00",
  nome: "João Silva",
  telefone: "(11) 99999-9999",
  endereco: "Rua das Flores, 123",
  email: "joao@email.com",
  senha: "senha123",
  genero: "M",
  data_nascimento: "1990-01-01",
  preferencias: "Tênis esportivo"
});

// 2. Fazer login
const loginData = await login("joao@email.com", "senha123");

// 3. Acessar perfil protegido
const perfil = await getClienteProfile();

// 4. Atualizar dados
const dadosAtualizados = await updateClienteProfile({
  nome: "João Silva Santos",
  telefone: "(11) 88888-8888"
});

// 5. Fazer logout
logout();
```

## Troubleshooting

### Problemas Comuns

**Erro 401 - Credenciais inválidas**
- Verificar se email e senha estão corretos
- Verificar se o usuário está ativo

**Erro 403 - Acesso negado**
- Verificar se o token é válido
- Verificar se o usuário tem permissão para a ação

**Erro 409 - Conflito**
- Email, CPF ou telefone já cadastrado

**Token expirado**
- Usar refresh token para obter novo access token
- Se refresh token expirou, fazer login novamente

## Próximos Passos

1. **Implementar recuperação de senha**
2. **Adicionar verificação de email**
3. **Implementar autenticação 2FA**
4. **Adicionar logs de auditoria**
5. **Implementar blacklist de tokens** 