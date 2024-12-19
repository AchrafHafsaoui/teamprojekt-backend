# driving_schedule/serializers.py
from rest_framework import serializers
from .models import DrivingSchedule, LocationType

class DrivingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingSchedule
        fields = ['id', 'bus', 'departure_time', 'arrival_time','departure_location' ,'dep_location_name' , 'arrival_location', 'arr_location_name']
class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ["id", "basis_version", "type_number", "short_code", "description"]
