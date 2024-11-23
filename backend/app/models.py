from django.db import models

# Create your models(database models) here.

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# TODO : add a joint table
class Vehicle(Base):
    __tablename__ = 'vehicles'

    vehicle_type = Column(String, nullable=False)  # Used for polymorphism
    license_plate = Column(String, unique=True, primary_key=True, nullable=False)
    date_of_purchase = Column(String, nullable=False)
    electric_capacity = Column(Float, nullable=False)
    state_of_charge = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    distance_left = Column(Float, nullable=True)
    station_number = Column(int, nullable=True)
    charging_point = Column(int, nullable=True)
    coming_from = Column(String, nullable=True)
    going_to = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'vehicle',  # Identity for the base class
        'polymorphic_on': vehicle_type      # Column storing type info
    }

class Bus(Vehicle):
    seat_capacity = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'bus'      # Identity for Bus
    }





