from django.db import models
from busMonitoring.models import ElectricBus

class LocationType(models.Model):
    description = models.CharField(max_length=60)  # Full description (e.g., "Haltepunkt")
    location_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.description} - {self.location_name}"
    
class DrivingSchedule(models.Model):
    bus = models.ForeignKey(
        ElectricBus,
        on_delete=models.CASCADE,
        related_name="driving_schedules",
        null=True,
        blank=True
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
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
        return f"Bus {self.bus.bus_id if self.bus else 'No Bus'} - Departure: {self.departure_location.location_name if self.departure_location else 'Unknown'} - Arrival: {self.arrival_location.location_name if self.arrival_location else 'Unknown'}"
