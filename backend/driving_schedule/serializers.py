# driving_schedule/serializers.py
from rest_framework import serializers
from .models import DrivingSchedule

class DrivingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingSchedule
        fields = ['bus_id','departure_time', 'arrival_time']
