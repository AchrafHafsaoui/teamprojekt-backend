from django.db import models

class LocationType(models.Model):
    basis_version = models.IntegerField()  # Version number
    type_number = models.IntegerField()  # Type ID
    short_code = models.CharField(max_length=8)  # Abbreviation (e.g., "HP", "OM")
    description = models.CharField(max_length=60)  # Full description (e.g., "Haltepunkt")

    def __str__(self):
        return f"{self.short_code} - {self.description}"
    
class DrivingSchedule(models.Model):
    bus_id = models.CharField(max_length=20)  # Unique identifier for the bus
    departure_time = models.DateTimeField()  # Scheduled departure time
    arrival_time = models.DateTimeField()  # Scheduled arrival time
    location_name = models.CharField(max_length=100,  null=True, blank=True)
    location_type = models.ForeignKey(
        LocationType, on_delete=models.CASCADE, related_name="schedules", null=True, blank=True)
    def __str__(self):
       return f"Bus {self.bus_id} - {self.location_name} ({self.location_type.short_code})"

