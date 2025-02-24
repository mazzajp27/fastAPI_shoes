from fastapi import FastAPI, HTTPException

import json

app = FastAPI()

def load_data():
    with open('dados.json', 'r') as file:
        return json.load(file)


@app.get("/")
def home():
    data = load_data() 
    return {"Shoes": len(data)}

@app.get("/shoes")
def get_shoes():
    data = load_data()
    return data


@app.get("/shoes/{id_shoe}")
def get_shoe(id_shoe: int):
    data = load_data()
    shoes = next((shoes for shoes in data if shoes["id"] == id_shoe), None)
    if shoes is None:
        raise HTTPException(status_code=404, detail="User not found")
    return shoes
    
@app.post("/shoes")
def add_shoe(shoe: dict):
    data = load_data()
    shoe["id"] = max(shoe["id"] for shoe in data) + 1 if data else 1
    data.append(shoe)
    with open('dados.json', 'w') as file:
        json.dump(data, file, indent=4)
    return shoe
