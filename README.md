# fastAPI_shoes
Criação de api com FastAPI hello world
fazendo alteração
### Para iniciar a aplicação digite o comando abaixo no diretório fastAPI_shoes/
uvicorn app.main:app --reload

```bash

/fastAPI_shoes/
│
├── app/
│   ├── __init__.py
│   ├── main.py        # Onde fica o app FastAPI e inicializa tudo
│   ├── crud/
│   │   ├── __init__.py
│   │   └── shoes.py   # Funções de banco: criar, listar, editar tênis
│   ├── models/
│   │   ├── __init__.py
│   │   └── shoes.py   # Model Shoes
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── shoes.py   # Pydantic BaseModel para validar entrada/saída
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes_shoes.py  # As rotas (endpoints) que chamam o CRUD
│   └── database.py    # Conexão e criação do banco
│   ├── testes/
│
├── env_exemplo.txt   # Exemplo para listar as variáveis de ambiente 
├── requirements.txt  # Dependências do projeto
├── .gitignore        # Arquivo que define o que o Git deve ignorar 
└── README.md          # explicações

```

## database.py
- configura string de conexao ao banco

