from fastapi import FastAPI , Path , HTTPException 
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

cars = {}


@app.get("/car-details/{skuID}/{name}")
def get_cars_details(skuID: int = Path(description="this is for id"),name: str = Path(description="this is for name")):
    for car in cars.values():
        if car["skuID"] == skuID and car["name"].lower() == name.lower():
            return car
        
@app.get("/get-car-by-model")
def get_car_by_year(model: Optional[str] = None):
    for car in cars:
        if model is None:
            return {"message": "Model parameter is required"}
        if cars[car]["model"].lower() == model.lower():
            return cars[car]
    raise HTTPException(status_code=404, detail="Car not found")



class Item(BaseModel):
    skuID: int
    name: str
    model: str
    year: int

@app.post("/add-car/{item_id}")
def add_car(item_id: int, item: Item):
    if item_id in cars:
        return {"message": "Item already exists"}
    cars[item_id] = item.dict()
    return cars[item_id]


class UpdateItem(BaseModel):
    skuID: Optional[int] = None
    name: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

@app.put("/update/car")
def update_car(item_id: int, item: UpdateItem):
    if item_id not in cars:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.skuID is not None:
        cars[item_id]["skuID"] = item.skuID
    if item.name is not None:
        cars[item_id]["name"] = item.name
    if item.model is not None:
        cars[item_id]["model"] = item.model
    if item.year is not None:
        cars[item_id]["year"] = item.year
    
    return cars[item_id]


@app.delete("/delete-car/{item_id}")
def delete_car(item_id: int = Path(description="ID of the car to delete")):
    if item_id not in cars:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = cars.pop(item_id)
    return {"message": "Item deleted successfully", "item": deleted_item}