import polars as pl

file_path = 'buses.parquet'

# Define the Bus class
class Bus:
    def __init__(self, vehicle_type, license_plate, date_of_purchase, electric_capacity, seat_capacity, state_of_charge, status):
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
        self.date_of_purchase = date_of_purchase
        self.electric_capacity = electric_capacity
        self.seat_capacity = seat_capacity
        self.state_of_charge = state_of_charge
        self.status = status

    @staticmethod
    def get(license_plate):
        # Retrieve a bus from the Parquet file by license_plate
        buses = pl.scan_parquet(file_path)
        buses = buses.filter(pl.col("license_plate") == license_plate).collect()
        print(buses)

    def save(self):
        # Placeholder for save logic
        pass

    @staticmethod
    def delete(license_plate):
        # Placeholder for delete logic
        pass


# Define the Station class
class Station:
    def __init__(self, number, electric_capacity, state_of_charge, status, occupied_stations):
        self.number = number
        self.electric_capacity = electric_capacity
        self.state_of_charge = state_of_charge
        self.status = status
        self.occupied_stations = occupied_stations


