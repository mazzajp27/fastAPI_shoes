from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

def load_data():
    with open('dados.json', 'r') as file:
        return json.load(file)

class Shoes(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    quantity: Optional[int] = None

@app.get("/")
def get_shoes():
    """Essa rota retorna a lista de todos os tenis e seus detalhes"""
    data = load_data()
    return data

@app.get("/qtd_shoes")
def home():
    """Essa rota retorna somente a quantidade de tenis que possui no banco"""
    data = load_data() 
    return {"Shoes": len(data)}


@app.get("/shoes/{id_shoe}")
def get_shoe(id_shoe: int):
    """Essa rota retorna um tenis pelo ID respectivo do tenis"""
    data = load_data()
    shoes = next((shoes for shoes in data if shoes["id"] == id_shoe), None)
    if shoes is None:
        raise HTTPException(status_code=404, detail="Shoes not found")
    return shoes
    
@app.post("/shoes")
def add_shoe(shoe: Shoes):
    """Essa rota faz um input dentro da base de dados de acordo com as características dos tenis"""
    data = load_data()
    new_id = max([item["id"] for item in data], default=0) + 1
    new_shoe = {"id": new_id, **shoe.dict()}
    new_shoe = dict(sorted(new_shoe.items(), key=lambda x: x[0] != "id"))
    data.append(new_shoe)
    with open('dados.json', 'w') as file:
        json.dump(data, file, indent=4)
    return shoe

@app.put("/shoes/{id_shoe}")
def put_shoe(id_shoe: int, shoe: Shoes):
    data = load_data()
    for index, item in enumerate(data):
        if item["id"] == id_shoe:
            data[index] = {"id": id_shoe, **shoe.dict()}
            with open('dados.json', 'w') as file:
                json.dump(data, file, indent=4)
            return shoe
    return {}