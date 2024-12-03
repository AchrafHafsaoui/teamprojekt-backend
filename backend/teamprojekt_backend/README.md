## This project uses the **Django framework**.

## Apps in Django

Apps are modular components that encapsulate specific functionality (e.g., pages, admin/user rights) for the project. Each app is designed to handle a specific area of the website or application.

### Managing Apps

1. **Declaring Apps**  
   All apps must be declared in the `INSTALLED_APPS` section of the `teamprojekt_backend/settings.py` file. Example:

   ```python
   INSTALLED_APPS = [
       ...
       'your_app_name',
   ]

   ```

2. **Creating an App**
   To create a new app, use the following steps:

   $ cd teamprojekt_backend
   $ python manage.py startapp <Name_of_Your_App>

# EXAMPLE USAGE

# Assuming you have an active SQLAlchemy session `db`

# Creating a Vehicle

vehicle_data = {
'license_plate': 'VEH1234',
'date_of_purchase': '2021-05-20',
'status': 'active',
'state_of_charge': 75.0,
'electric_capacity': 150.0,
'vehicle_type': 'vehicle',
}
new_vehicle = VehicleCRUD.create_vehicle(db, vehicle_data)

# Creating a Bus

bus_data = {
'license_plate': 'BUS5678',
'date_of_purchase': '2022-08-15',
'status': 'in_service',
'state_of_charge': 85.0,
'electric_capacity': 200.0,
'vehicle_type': 'bus',
'seat_capacity': 50,
}
new_bus = VehicleCRUD.create_bus(db, bus_data)

# Updating a vehicle by certain param

updates = {
'status': 'inactive',
'state_of_charge': 50.0,
}
vehicle = db.query(Vehicle).filter_by(license_plate='VEH1234').first()
updated_vehicle = VehicleCRUD.update_vehicle(db, vehicle, updates)

Rules for depot management (src= Charging Schedule for Load Peak Minimization on Large-Scale Electric Bus Depots; this is a reseach paper made in Hamburg for the Alsterdorf depot station managing over 127 buses doing 230 trips daily )

Route assigning:

1. Bus cannot take a route if the expected state-of-charge (SoC) upon its return to the depot will be
   smaller than 20%.
2. Bus needs to match the bus type necessary for the trip (standard, articulated)
3. the charging station. It is not possible to charge buses at any other level between 0 and 150 kW.
   An additional power consumption occurs during the preconditioning time. This is the electrical heating of the bus before it leaves the depot. It is assumed that the bus needs to heat for X minutes( 2hours at -15degree temp and 15 mins at 28degree ) prior to its departure if it was parked at the depot for longer than two hours

Charging and preconditioning:

- Before electric buses are going into daily public transport service, energy-consuming activities like heating the bus interior should be done at the bus depot while the bus is still connected to the grid
- Preconditioning blocks are fixed in time and cannot be moved. Charging blocks can be freely moved in the time window between the arrival and departure time.
- Approximately half an hour for pre-conditioning.

1#PRECONDITIONING:

# Fetch all departures

# Schedule all preconditioning orders

# Calculate §bus for all buses in Buses (with §b= arrival_time - departure_time - length_of_charging)

# Arrange Buses ascending by §b

# Initialize i=1

#### If i <= n:

        # bus = Buses(i)
        # Calculate Pbus
        # Calculate Hmax for all charging intervals in range Pbus (Hmax i peak demand in a certain time)
        # Choose Cbus as a tuple of charging intervals from P bus with the least Hmax
        # If |Cbus| > 1
            # Redefine Cbus as a tuple of charging intervals from Cbus with the least Hinterval
            # If |Cbus| > 1
                # Redefine Cbus as the charging interval from Cbus with the earliest charging start s
    # C bus is the chosen charging interva for bus

# i += 1
