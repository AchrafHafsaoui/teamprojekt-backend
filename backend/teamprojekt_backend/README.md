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


for the db management we chose to go with db polymorfism from sqlalchemy library, this will help us have a parent group named vehicle where data will be saved, and in this db there we bill the many vehicle types(Bus and maybe other types of vehicles in our case), we have seen for now that the similarities are not too many(like seat capacity in our case) so we decided to put the data in a single file, but we can use table splitting, where we save only the shared between vehicles and save the difference(special charasteristics) in a split table where it is to joined with the specific table per vehicle type. Each method has pros and cons but for now this seems optimal for the time complexity and reliability.

                     [ VEHICLE TABLE ] (Parent Table)
                  +------------------------+
                  | id(license plate) (PK)|
                  | vehicle_type          |  <-- Discriminator column (e.g., 'Bus', 'Car')
                  | shared_attribute_1    |  <-- Attributes shared across all vehicles
                  | shared_attribute_2    |
                  +------------------------+
                              |
                              +---------------------------------------+
                              |                                       |
                  [ BUS TABLE ] (Child Table)                [ CAR TABLE ] (Child Table)
                  +------------------------+                 +------------------------+
                  | id (FK to VEHICLE.id)  |                 | id (FK to VEHICLE.id)  |
                  | seat_capacity          |                 | trunk_size             |
                  | special_bus_feature    |                 | special_car_feature    |
                  +------------------------+                 +------------------------+


# TODO:

install POSTGRESQL on docker

change DATABASES file in team_projekt/settings.py to add POSTGRESQL db