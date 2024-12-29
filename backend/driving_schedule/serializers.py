# driving_schedule/serializers.py
from rest_framework import serializers
from .models import DrivingSchedule, LocationType
from busMonitoring.models import ElectricBus

class ElectricBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricBus
        fields = ['bus_id', 'battery_capacity', 'length']

class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = [ "location_name", "description"]
class DrivingScheduleSerializer(serializers.ModelSerializer):
    departure_location = LocationTypeSerializer()
    arrival_location = LocationTypeSerializer()
    bus = ElectricBusSerializer()
    class Meta:
        model = DrivingSchedule
        fields = ['id', 'bus', 'departure_time', 'arrival_time','departure_location' , 'arrival_location']

