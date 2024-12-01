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
   An additional power consumption occurs during the preconditioning time. This is the electrical heating of the bus before it leaves the depot. It is assumed that the bus needs to heat for X minutes( 2hours at -15degree temp in the article ) prior to its departure if it was parked at the depot for longer than two hours

Charging and preconditioning:

- Before electric buses are going into daily public transport service, energy-consuming activities like heating the bus interior should be done at the bus depot while the bus is still connected to the grid
- Preconditioning blocks are fixed in time and cannot be moved. Charging blocks can be freely moved in the time window between the arrival and departure time.
- Approximately half an hour for pre-conditioning.

1. This algorithm uses a simple greedy logic. It defines a limit for the maximum allowed height t_max.The algorithm chooses the charging intervals for each bus, so that the 𝐻_max <= t_max .The limit t_max is reduced iteratively as long as it is possible to schedule all charging jobs. The smallest limit for which the algorithm manages to schedule all jobs is considered the minimum peak demand.
2. Before executing the algorithm, the following steps are required:
   - step1: Schedule all preconditioning jobs(Based or departure times, each bus need x amount of time before departing, changeable as the depot manager wishes)
   - step2: Calculate all possible charging intervals for n first buses to leave buses ( with n= number of charging ports ) and write them into tuples p
   - step3: Organize all buses ascending by the arrival time
   - step4: Initialize the limit t_max = c\*number of buses to charge (with c= curtailment factor (The curtailment factor c is a limit for the number of buses that can charge simultaneously without affecting the charging process itself. An example that for 127 buses at the depot, the curtailment factor is 54%, meaning the grid wants to spend a charging capacity of 68 buses simultaneously. t_max is therefore initialized with c=054))
