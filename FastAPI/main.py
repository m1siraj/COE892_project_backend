from fastapi import FastAPI, HTTPException
from typing import List, Tuple
from models import Warehouse, DeliveryVehicle, Order
from database import Database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Replace with your React app's URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

db = Database()

@app.get("/warehouse/", response_model=List[Warehouse])
async def get_warehouses():
    return list(db.warehouses.values())

@app.post("/warehouse/", response_model=Warehouse)
async def create_warehouse(warehouse: Warehouse):
    try:
        # Check if warehouse with the same ID already exists
        if db.get_warehouse(warehouse.id):
            raise HTTPException(status_code=409, detail="Warehouse with the same ID already exists")
        
        # Validate current capacity
        if warehouse.current_capacity > warehouse.max_capacity:
            raise HTTPException(status_code=422, detail="Current capacity cannot exceed maximum capacity")
        
        # Validate warehouse data
        if warehouse.location[0] < -90 or warehouse.location[0] > 90 \
                or warehouse.location[1] < -180 or warehouse.location[1] > 180:
            raise HTTPException(status_code=422, detail="Invalid warehouse location")

        # Perform database operation to create warehouse
        created_warehouse = db.create_warehouse(warehouse)
        
        # Return created warehouse
        return created_warehouse

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error occurred while creating warehouse: {e}")
        # Raise HTTPException with 500 status code
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/warehouse/{warehouse_id}", response_model=Warehouse)
async def get_warehouse(warehouse_id: int):
    warehouse = db.get_warehouse(warehouse_id)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@app.delete("/warehouse/{warehouse_id}")
async def delete_warehouse(warehouse_id: int):
    # db.delete_warehouse(warehouse_id)
    # return {"message": "Warehouse deleted successfully"}
    try:
        db.delete_warehouse(warehouse_id)
        return {"message": "Warehouse deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Warehouse not found")

@app.get("/vehicle/", response_model=List[DeliveryVehicle])
async def get_vehicles():
    return list(db.vehicles.values())

@app.post("/vehicle/", response_model=DeliveryVehicle)
async def create_vehicle(vehicle: DeliveryVehicle):
    print(vehicle)
    return db.create_vehicle(vehicle)

@app.get("/vehicle/{vehicle_id}", response_model=DeliveryVehicle)
async def get_vehicle(vehicle_id: int):
    vehicle = db.get_vehicle(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
    # return [vehicle.dict() for vehicle in db.vehicles.values()]

@app.delete("/vehicle/{vehicle_id}")
async def delete_vehicle(vehicle_id: int):
    # db.delete_vehicle(vehicle_id)
    # return {"message": "Vehicle deleted successfully"}
    try:
        db.delete_vehicle(vehicle_id)
        return {"message": "Vehicle deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Vehicle not found")

# Endpoint to create orders
@app.post("/orders/", response_model=Order)
async def create_order(orders: Order):
    # Validate selected warehouse
    selected_warehouse = next((w for w in list(db.warehouses.values()) if w.id == orders.warehouse_id), None)
    if not selected_warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    # Validate selected vehicle
    selected_vehicle = next((v for v in list(db.vehicles.values()) if v.id == orders.vehicle_id), None)
    if not selected_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Check if vehicle coverage area contains the location of the warehouse
    if not any(selected_warehouse.location == coverage_area for coverage_area in selected_vehicle.coverage_area):
        raise HTTPException(status_code=422, detail="Vehicle coverage area does not contain warehouse location")

    # Calculate new current capacity for the warehouse
    new_current_capacity = selected_warehouse.current_capacity + orders.quantity

    # Check if new current capacity exceeds maximum capacity of the warehouse
    if new_current_capacity > selected_warehouse.max_capacity:
        raise HTTPException(status_code=422, detail="Current capacity exceeds maximum capacity of the warehouse")

    # Update current capacity of the warehouse
    selected_warehouse.current_capacity = new_current_capacity
    
    # Perform database operation to create warehouse
    created_order = db.create_order(orders)
    
    # Return the created order
    return created_order

@app.get("/orders/", response_model=List[Order])
async def get_orders():
    return list(db.orders.values())
    # return [order.dict() for order in db.orders.values()]
    
@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    order = db.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    try:
        db.delete_order(order_id)
        return {"message": "Order deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")