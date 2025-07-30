# Usa uma imagem oficial com Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /code

# Copia os arquivos para o contêiner
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta usada pelo FastAPI
EXPOSE 8000

# Comando para iniciar o FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
