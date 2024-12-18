# driving_schedule/serializers.py
from rest_framework import serializers
from .models import DrivingSchedule, LocationType
from busMonitoring.models import ElectricBus

class DrivingScheduleSerializer(serializers.ModelSerializer):
    bus = serializers.PrimaryKeyRelatedField(queryset=ElectricBus.objects.all())

    class Meta:
        model = DrivingSchedule
        fields = ['id', 'bus', 'departure_time', 'arrival_time', 'location_name', 'location_type']
class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ["id", "basis_version", "type_number", "short_code", "description"]
