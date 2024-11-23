class Vehicle:
    def __init__(self, license_plate: str, date_of_purchase: str, status: str, state_of_charge: float, electric_capacity: float, vehicle_type: str):
        self.license_plate = license_plate
        self.date_of_purchase = date_of_purchase
        self.status = status
        self.state_of_charge = state_of_charge
        self.electric_capacity = electric_capacity
        self.vehicle_type = vehicle_type

    def save_to_database(self, db_manager):
        conn = db_manager.connect()
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO vehicles (license_plate, date_of_purchase, status, state_of_charge, electric_capacity, vehicle_type) VALUES (?, ?, ?, ?, ?, ?)",
            (self.license_plate, self.date_of_purchase, self.status, self.state_of_charge, self.electric_capacity, self.vehicle_type)
        )
        conn.commit()
        print(f"Vehicle '{self.license_plate}' saved to database.")

    def delete_from_database(self, db_manager):
        conn = db_manager.connect()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM vehicles WHERE license_plate = ?",
            (self.license_plate,)
        )
        conn.commit()
        print(f"Vehicle '{self.license_plate}' deleted from database.")

    def edit_attribute(self, db_manager, param, value):
        if hasattr(self, param):
            setattr(self, param, value)
            conn = db_manager.connect()
            cur = conn.cursor()
            cur.execute(
                f"UPDATE vehicles SET {param} = ? WHERE license_plate = ?",
                (value, self.license_plate)
            )
            conn.commit()
            print(f"Vehicle '{self.license_plate}' updated: {param} = {value}")
        else:
            print(f"Attribute {param} does not exist on Vehicle.")

class Bus(Vehicle):
    def __init__(self, license_plate: str, date_of_purchase: str, status: str, 
                 state_of_charge: float, electric_capacity: float, seat_capacity: int):
        super().__init__(license_plate, date_of_purchase, status, state_of_charge, electric_capacity, "Bus")
        self.seat_capacity = seat_capacity

    def save_to_database(self, db_manager):
        super().save_to_database(db_manager)
        conn = db_manager.connect()
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO buses (license_plate, seat_capacity) VALUES (?, ?)",
            (self.license_plate, self.seat_capacity)
        )
        conn.commit()
        print(f"Bus '{self.license_plate}' additional data saved to database.")

# Example Usage
db_manager = ...  # Assume this is your database manager object
bus = Bus("123-XYZ", "2023-01-01", "active", 80.0, 100.0, 50)
bus.save_to_database(db_manager)
