from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modelo de datos
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# Base de datos simulada con datos pre-cargados
db = [
    Item(id=1, name="Laptop", description="Potente laptop para programación", price=1200.00),
    Item(id=2, name="Smartphone", description="Último modelo con cámara de alta resolución", price=800.00),
    Item(id=3, name="Tablet", description="Perfecta para trabajo y entretenimiento", price=500.00),
    Item(id=4, name="Auriculares", description="Auriculares inalámbricos con cancelación de ruido", price=150.00),
    Item(id=5, name="Monitor", description="Monitor 4K de 27 pulgadas", price=350.00)
]

@app.get("/")
async def root():
    return {"message": "Bienvenido a mi API con FastAPI", "items_count": len(db)}

@app.get("/items", response_model=List[Item])
async def get_items():
    return db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((item for item in db if item.id == item_id), None)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    if any(x.id == item.id for x in db):
        raise HTTPException(status_code=400, detail="ID ya existe")
    db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    index = next((index for index, i in enumerate(db) if i.id == item_id), None)
    if index is not None:
        db[index] = item
        return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    index = next((index for index, i in enumerate(db) if i.id == item_id), None)
    if index is not None:
        deleted_item = db.pop(index)
        return {"message": f"Item '{deleted_item.name}' eliminado"}
    raise HTTPException(status_code=404, detail="Item no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
