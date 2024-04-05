from typing import List, Tuple
from pydantic import BaseModel

class Warehouse(BaseModel):
    id: int
    name: str
    location: Tuple[int, int]
    max_capacity: int
    current_capacity: int

class DeliveryVehicle(BaseModel):
    id: int
    name: str
    coverage_area: List[Tuple[int, int]]

class Order(BaseModel):
    order_id: int
    order_name: str
    warehouse_id: int
    vehicle_id: int
    quantity: int