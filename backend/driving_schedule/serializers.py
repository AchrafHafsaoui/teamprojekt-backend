# driving_schedule/serializers.py
from rest_framework import serializers
from .models import DrivingSchedule, LocationType

class DrivingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingSchedule
        fields = ['id', 'bus', 'departure_time', 'arrival_time','departure_location' , 'arrival_location']
class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ["id", "location_name", "description"]
