from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Vehicle, Bus

class VehicleCRUD:

    @staticmethod
    def create_vehicle(db: Session, vehicle_data: dict) -> Vehicle:
        # Create and return a new vehicle ( vehicle is parent class of Bus and ...)
        try:
            vehicle = Vehicle(**vehicle_data)
            db.add(vehicle)
            db.commit()
            db.refresh(vehicle)
            return vehicle
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Vehicle with license_plate '{vehicle_data['license_plate']}' already exists.")
    
    @staticmethod
    def get_vehicle_by_license_plate(db: Session, license_plate: str) -> Vehicle:
        # Retrieve a vehicle by license plate
        vehicle = db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
        if not vehicle:
            raise ValueError(f"No vehicle found with license_plate '{license_plate}'.")
        return vehicle

    @staticmethod
    def update_vehicle(db: Session, vehicle: Vehicle, updates: dict) -> Vehicle:
        # Update attributes of a vehicle
        for key, value in updates.items():
            if hasattr(vehicle, key):
                setattr(vehicle, key, value)
            else:
                raise ValueError(f"Attribute '{key}' does not exist on Vehicle.")
        db.commit()
        db.refresh(vehicle)
        return vehicle
    
    @staticmethod
    def delete_vehicle(db: Session, vehicle: Vehicle):
        # Delete a vehicle
        db.delete(vehicle)
        db.commit()


class BusCRUD:

    @staticmethod
    def get_bus_by_license_plate(db: Session, license_plate: str) -> Bus:
        # Retrieve a vehicle by license plate
        bus = db.query(Bus).filter(Bus.license_plate == license_plate).first()
        if not bus:
            raise ValueError(f"No bus found with license_plate '{license_plate}'.")
        return bus
    
    @staticmethod
    def create_bus(db: Session, bus_data: dict) -> Bus:
        # Create and return a new bus
        try:
            bus = Bus(**bus_data)
            db.add(bus)
            db.commit()
            db.refresh(bus)
            return bus
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Bus with license_plate '{bus_data['license_plate']}' already exists.")

    @staticmethod
    def update_bus(db : Session, bus: Bus, updates: dict) -> Bus:
        # Update attributes of a bus
        for key, value in updates.items():
            if hasattr(bus, key):
                setattr(Bus, key, value)
            else:
                raise ValueError(f"Attribute '{key}' does not exist on Bus.")
        db.commit()
        db.refresh(bus)
        return bus

    @staticmethod
    def delete_bus(db: Session, bus: Bus):
        # Delete a vehicle
        db.delete(bus)
        db.commit()    
    



