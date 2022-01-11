# Serving our API via hypercorn
import asyncio
import hypercorn
from hypercorn.asyncio import serve

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Fake Database
class Database:
    def __init__(self):
        self.warehouses = {}

    def get_names(self):
        return list(self.warehouses.keys())

    def create_new(self, name: str, location: str, capacity: int):
        self.warehouses[name] = {
            "name": name,
            "location": location,
            "capacity": capacity
        }

    def get_by_name(self, name: str):
        return self.warehouses[name]

    def update_by_name(self, old_name: str, new_name: str, location: str, capacity: int):
        self.warehouses[old_name] = {
            "name" : new_name,
            "location":location,
            "capacity":capacity
        }

    def delete_by_name(self, name: str):
        del self.warehouses[name]


warehouse_database = Database()
warehouse_database.create_new("Test", "Prague", 100)


# Warehouse Model
class WarehouseDto(BaseModel):
    name: str
    location: str
    capacity: int


# Designing API
app = FastAPI()


@app.get("/warehouse")
def get_warehouse_names():
    # return all names of my warehouses
    return warehouse_database.get_names()


@app.post("/warehouse")
def create_warehouse(warehouse: WarehouseDto):
    # check if warehouse exists, if yes, return error
    if warehouse.name in warehouse_database.get_names():
        # warehouse already exists raise error
        raise HTTPException(409, detail="Name already exists!")

    # creates new warehouse
    warehouse_database.create_new(
        name=warehouse.name,
        location=warehouse.location,
        capacity=warehouse.capacity,
    )


@app.get("/warehouse/{warehouse_name}", response_model=WarehouseDto)
def get_warehouse_by_name(warehouse_name: str):
    if warehouse_name not in warehouse_database.get_names():
        # warehouse already exists raise error
        raise HTTPException(404, detail="I can not find this name!")
    # get warehouse by name
    warehouse = warehouse_database.get_by_name(warehouse_name)
    return WarehouseDto(
        name=warehouse["name"],
        location=warehouse["location"],
        capacity=warehouse["capacity"],
    )


@app.put("/warehouse/{warehouse_name}")
def update_warehouse_by_name(warehouse_name: str, warehouse: WarehouseDto):
    # YOUR CODE HERE
    if warehouse_name not in warehouse_database.get_names():
        raise HTTPException(404, detail="I can not update this object")
    warehouse_database.update_by_name(warehouse_name, warehouse.name, warehouse.location, warehouse.capacity)


@app.delete("/warehouse/{warehouse_name}")
def delete_warehouse_by_name(warehouse_name: str):
    if warehouse_name not in warehouse_database.get_names():
        raise HTTPException(404, detail="I cannot find this object to delete")
    warehouse_database.delete_by_name(warehouse_name)


app_config = hypercorn.config.Config()
app_config.use_reloader = True
asyncio.run(serve(app, app_config))
