from fastapi import FastAPI
app = FastAPI()


vendas = {
    1:{"item":"lata", "preco-unitario": 4,"quantidade":5},
    2:{"item":"garrafa 1L", "preco-unitario": 15,"quantidade":5},
    3:{"item":"garrafa 750ml", "preco-unitario": 10,"quantidade":5},
    4:{"item":"lata mini", "preco-unitario": 2,"quantidade":5},
}

@app.get("/")
def home():
    return {"Vendas": len(vendas)}

@app.get("/vendas/{id_venda}")
def pegar_venda(id_venda: int):
    if id_venda in vendas:
        return vendas[id_venda]
    else:
        return{"Erro": "ID Venda inexistente"}