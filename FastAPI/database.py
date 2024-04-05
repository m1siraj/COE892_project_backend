from typing import Dict, Tuple
from models import Warehouse, DeliveryVehicle, Order

class Database:
    warehouses: Dict[int, Warehouse] = {}
    vehicles: Dict[int, DeliveryVehicle] = {}
    orders: Dict[int, Order] = {}
    
    def __init__(self):
        self.create_sample_data()
        
    def create_sample_data(self):
        # Create sample warehouses
        warehouse1 = Warehouse(id=1, name="Warehouse A", location=(40, -74), max_capacity=100, current_capacity=50)
        warehouse2 = Warehouse(id=2, name="Warehouse B", location=(34, -118), max_capacity=150, current_capacity=100)
        warehouse3 = Warehouse(id=3, name="Warehouse C", location=(44, -218), max_capacity=150, current_capacity=100)
        warehouse4 = Warehouse(id=4, name="Warehouse D", location=(345, -518), max_capacity=150, current_capacity=100)
        self.warehouses[1] = warehouse1
        self.warehouses[2] = warehouse2
        self.warehouses[3] = warehouse3
        self.warehouses[4] = warehouse4

        # Create sample delivery vehicles
        vehicle1 = DeliveryVehicle(id=1, name="Vehicle X", coverage_area=[(40, -74), (42, -72)])
        vehicle2 = DeliveryVehicle(id=2, name="Vehicle Y", coverage_area=[(34, -118), (34, -118)])
        self.vehicles[1] = vehicle1
        self.vehicles[2] = vehicle2

    def get_warehouse(self, warehouse_id: int) -> Warehouse:
        return self.warehouses.get(warehouse_id)

    def create_warehouse(self, warehouse: Warehouse) -> Warehouse:
        if warehouse.id in self.warehouses:
            raise ValueError("Warehouse ID already exists")
        self.warehouses[warehouse.id] = warehouse
        return warehouse

    def delete_warehouse(self, warehouse_id: int):
        if warehouse_id not in self.warehouses:
            raise ValueError("Warehouse ID does not exist")
        del self.warehouses[warehouse_id]

    def get_vehicle(self, vehicle_id: int) -> DeliveryVehicle:
        return self.vehicles.get(vehicle_id)

    def create_vehicle(self, vehicle: DeliveryVehicle) -> DeliveryVehicle:
        if vehicle.id in self.vehicles:
            raise ValueError("Vehicle ID already exists")
        self.vehicles[vehicle.id] = vehicle
        return vehicle

    def delete_vehicle(self, vehicle_id: int):
        if vehicle_id not in self.vehicles:
            raise ValueError("Vehicle ID does not exist")
        del self.vehicles[vehicle_id]
        
    def update_warehouse_capacity(self, warehouse_id: int, qty: int):
        warehouse = self.get_warehouse(warehouse_id)
        if not warehouse:
            raise ValueError("Warehouse not found")
        if warehouse.can_fulfill_order(qty):
            warehouse.current_capacity += qty
        else:
            raise ValueError("Order quantity exceeds warehouse capacity")

    def can_vehicle_cover_warehouse(self, vehicle_id: int, warehouse_location: Tuple[int, int]) -> bool:
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        warehouse_location_set = set(warehouse_location)
        for coverage_point in vehicle.coverage_area:
            if set(coverage_point) == warehouse_location_set:
                return True
        return False
    
    def create_order(self, order: Order) -> Order:
        if order.order_id in self.orders:
            raise ValueError("Order ID already exists")  # Change warehouse to order
        self.orders[order.order_id] = order  # Change warehouses to orders
        # Update warehouse current capacity
        warehouse_id = order.warehouse_id
        warehouse = self.get_warehouse(warehouse_id)
        if not warehouse:
            raise ValueError("Warehouse not found")
        new_current_capacity = warehouse.current_capacity + order.quantity
        if new_current_capacity > warehouse.max_capacity:
            raise ValueError("Order quantity exceeds warehouse capacity")
        # warehouse.current_capacity = new_current_capacity
        return order
    
    def get_order(self, order_id: int) -> Order:
        return self.orders.get(order_id)
    
    def delete_order(self, order_id: int):
        if order_id not in self.orders:
            raise ValueError("Order ID does not exist")
        del self.orders[order_id]