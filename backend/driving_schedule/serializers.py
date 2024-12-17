# driving_schedule/serializers.py
from rest_framework import serializers
from .models import DrivingSchedule, LocationType

class DrivingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingSchedule
        fields = ["id", "bus_id", "location_name", "location_type", "arrival_time", "departure_time"]
class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ["id", "basis_version", "type_number", "short_code", "description"]
