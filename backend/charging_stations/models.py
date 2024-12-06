from django.db import models

class Station(models.Model):
    AVAILABILITY_CHOICES = [
        ("OK", "Available"),
        ("Down", "Out of Service"),
        ("Maintenance", "Under Maintenance"),
    ]
    
    station_id = models.CharField(max_length=10, unique=True)  # Unique identifier for each station
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES)  # Current status
    charging_power = models.FloatField()  # Current charging power in kW
    max_power = models.FloatField()  # Maximum charging power in kW
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-record creation time
    updated_at = models.DateTimeField(auto_now=True)  # Auto-record last update time

    def __str__(self):
        return self.station_id
