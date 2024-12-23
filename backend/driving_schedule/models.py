from django.db import models
from busMonitoring.models import ElectricBus

class LocationType(models.Model):
    basis_version = models.IntegerField()  # Version number
    description = models.CharField(max_length=60)  # Full description (e.g., "Haltepunkt")
    def __str__(self):
        return f"{self.short_code} - {self.description}"
    
class DrivingSchedule(models.Model):
    bus = models.ForeignKey(  # Updated field
        ElectricBus, 
        on_delete=models.CASCADE, 
        related_name="driving_schedules" , # Allows reverse querying from ElectricBus
        null=True, 
        blank=True
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    dep_location_name = models.CharField(max_length=100, null=True, blank=True)
    arr_location_name = models.CharField(max_length=100, null=True, blank=True)
    departure_location = models.ForeignKey(
        LocationType,
        on_delete=models.CASCADE,
        related_name="departure_schedules",
        null=True,
        blank=True
    )
    arrival_location = models.ForeignKey(
        LocationType,
        on_delete=models.CASCADE,
        related_name="arrival_schedules",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Bus {self.bus.bus_id} - {self.location_name} ({self.location_type.short_code if self.location_type else 'No Type'})"

