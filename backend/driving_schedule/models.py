from django.db import models

class DrivingSchedule(models.Model):
    bus_id = models.CharField(max_length=10)  # Unique identifier for the bus
    driver_name = models.CharField(max_length=100)  # Name of the driver
    route_id = models.CharField(max_length=10)  # Route identifier
    departure_time = models.DateTimeField()  # Scheduled departure time
    arrival_time = models.DateTimeField()  # Scheduled arrival time
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-record creation time
    updated_at = models.DateTimeField(auto_now=True)  # Auto-record last update time

    def __str__(self):
        return f"Bus {self.bus_id} on Route {self.route_id}"

