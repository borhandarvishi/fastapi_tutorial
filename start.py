from fastapi import FastAPI

app = FastAPI()

cars = {
    1: {"skuID":23,"name": "Toyota", "model": "Corolla", "year": 2020},
    2: {"skuID":43,"name": "Honda", "model": "Civic", "year": 2019},
}


@app.get("/car-details/{skuID}")
def get_cars_details(skuID: int):
    for car in cars.values():
        if car["skuID"] == skuID:
            return car
    return {"error": "Car not found"}