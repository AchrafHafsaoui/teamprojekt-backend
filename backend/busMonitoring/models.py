from django.db import models

class ElectricBus(models.Model):
    # Define the attributes for the bus
    vehicle_type = models.CharField(max_length=50)  # Type of vehicle
    bus_id = models.CharField(max_length=50, unique=True)  # Unique bus ID
    battery = models.FloatField()  # Battery level as a percentage
    charging_start = models.DateTimeField(null=True, blank=True)  # Charging start time, nullable
    status = models.CharField(
        max_length=20,
        choices=[
            ("In Depot", "In Depot"),
            ("Maintenance", "Maintenance"),
            ("On Route", "On Route"),
        ],
    )
    charging_location = models.CharField(
        max_length=50, null=True, blank=True
    )  # Location ID or null if not charging
    CAP = models.CharField(max_length=20)  # CAP (Capacity)
    ENE = models.CharField(max_length=20)  # ENE (Energy)

    def __str__(self):
        return f"{self.bus_id} - {self.status}"
