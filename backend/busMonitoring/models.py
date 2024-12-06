from django.db import models

class ElectricBus(models.Model):
    # Define the attributes for the bus
    bus_id = models.CharField(max_length=50, unique=True)  # Unique bus ID
    status = models.CharField(
        max_length=20,
        choices=[
            ("In Depot", "In Depot"),
            ("Maintenance", "Maintenance"),
            ("On Route", "On Route"),
        ],
    )
    battery = models.IntegerField()  # Battery level as a percentage
    session_start = models.DateTimeField(null=True, blank=True)  # Charging start time, nullable
    charging_point = models.CharField(
        max_length=50, null=True, blank=True
    )  # Location ID or null if not charging
    CAP = models.IntegerField()  # CAP (Capacity)
    ENE = models.IntegerField()  # ENE (Energy)

    def __str__(self):
        return f"{self.bus_id} - {self.status}"



