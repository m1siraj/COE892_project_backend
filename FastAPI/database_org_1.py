import json
import sqlite3
from typing import Dict, Tuple
from models import Warehouse, DeliveryVehicle, Order

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.initialize_data()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warehouses (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                location_x INTEGER,
                                location_y INTEGER,
                                max_capacity INTEGER,
                                current_capacity INTEGER
                             )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                coverage_area TEXT
                             )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                order_id INTEGER PRIMARY KEY,
                                order_name TEXT,
                                warehouse_id INTEGER,
                                vehicle_id INTEGER,
                                quantity INTEGER,
                                FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
                                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
                             )''')

        self.connection.commit()
        
    def initialize_data(self):
        self.cursor.execute('''SELECT * FROM warehouses''')
        warehouse_data = self.cursor.fetchall()
        self.warehouses = {row[0]: Warehouse(id=row[0], name=row[1], location=(row[2], row[3]),
                                             max_capacity=row[4], current_capacity=row[5]) for row in warehouse_data}

        self.cursor.execute('''SELECT * FROM vehicles''')
        vehicle_data = self.cursor.fetchall()
        self.vehicles = {row[0]: DeliveryVehicle(id=row[0], name=row[1], coverage_area=eval(row[2])) for row in vehicle_data}

        self.cursor.execute('''SELECT * FROM orders''')
        order_data = self.cursor.fetchall()
        self.orders = {row[0]: Order(order_id=row[0], order_name=row[1], warehouse_id=row[2],
                                      vehicle_id=row[3], quantity=row[4]) for row in order_data}

    def create_warehouse(self, warehouse: Warehouse):
        self.cursor.execute('''INSERT INTO warehouses (id, name, location_x, location_y, max_capacity, current_capacity)
                               VALUES (?, ?, ?, ?, ?, ?)''',
                            (warehouse.id, warehouse.name, warehouse.location[0], warehouse.location[1],
                             warehouse.max_capacity, warehouse.current_capacity))
        self.connection.commit()

    def create_vehicle(self, vehicle: DeliveryVehicle) -> DeliveryVehicle:
        coverage_area_str = json.dumps(vehicle.coverage_area)  # Serialize to JSON
        print('coverage_area_str')
        print(coverage_area_str)
        self.cursor.execute('''INSERT INTO vehicles (id, name, coverage_area)
                               VALUES (?, ?, ?)''',
                            (vehicle.id, vehicle.name, coverage_area_str))
        self.connection.commit()

    def create_order(self, order: Order):
        self.cursor.execute('''INSERT INTO orders (order_id, order_name, warehouse_id, vehicle_id, quantity)
                               VALUES (?, ?, ?, ?, ?)''',
                            (order.order_id, order.order_name, order.warehouse_id, order.vehicle_id, order.quantity))
        self.connection.commit()

    def delete_warehouse(self, warehouse_id: int):
        self.cursor.execute('''DELETE FROM warehouses WHERE id = ?''', (warehouse_id,))
        self.connection.commit()

    def delete_vehicle(self, vehicle_id: int):
        self.cursor.execute('''DELETE FROM vehicles WHERE id = ?''', (vehicle_id,))
        self.connection.commit()

    def delete_order(self, order_id: int):
        self.cursor.execute('''DELETE FROM orders WHERE order_id = ?''', (order_id,))
        self.connection.commit()

    def update_warehouse_capacity(self, warehouse_id: int, new_capacity: int):
        self.cursor.execute('''UPDATE warehouses SET current_capacity = ? WHERE id = ?''', (new_capacity, warehouse_id))
        self.connection.commit()

    def get_warehouse(self, warehouse_id: int) -> Warehouse:
        self.cursor.execute('''SELECT * FROM warehouses WHERE id = ?''', (warehouse_id,))
        warehouse_data = self.cursor.fetchone()
        if warehouse_data:
            return Warehouse(id=warehouse_data[0], name=warehouse_data[1], location=(warehouse_data[2], warehouse_data[3]),
                              max_capacity=warehouse_data[4], current_capacity=warehouse_data[5])
        return None

    def get_vehicle(self, vehicle_id: int) -> DeliveryVehicle:
        self.cursor.execute('''SELECT * FROM vehicles WHERE id = ?''', (vehicle_id,))
        vehicle_data = self.cursor.fetchone()
        if vehicle_data:
            return DeliveryVehicle(id=vehicle_data[0], name=vehicle_data[1], coverage_area=eval(vehicle_data[2]))
        return None

    def get_order(self, order_id: int) -> Order:
        self.cursor.execute('''SELECT * FROM orders WHERE order_id = ?''', (order_id,))
        order_data = self.cursor.fetchone()
        if order_data:
            return Order(order_id=order_data[0], order_name=order_data[1], warehouse_id=order_data[2],
                         vehicle_id=order_data[3], quantity=order_data[4])
        return None

    def close_connection(self):
        self.connection.close()
