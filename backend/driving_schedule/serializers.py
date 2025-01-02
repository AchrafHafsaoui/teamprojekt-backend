from rest_framework import serializers
from .models import DrivingSchedule, LocationType
from busMonitoring.models import ElectricBus

class ElectricBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricBus
        fields = ['id', 'bus_id', 'battery']

class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ["location_name", "description"]

class DrivingScheduleSerializer(serializers.ModelSerializer):
    # Input fields
    departure_location = serializers.PrimaryKeyRelatedField(queryset=LocationType.objects.all())
    arrival_location = serializers.PrimaryKeyRelatedField(queryset=LocationType.objects.all())
    bus = serializers.PrimaryKeyRelatedField(queryset=ElectricBus.objects.all())

    # Output fields
    departure_location_name = serializers.SerializerMethodField()
    arrival_location_name = serializers.SerializerMethodField()
    bus_details = ElectricBusSerializer(source="bus", read_only=True)

    def get_departure_location_name(self, obj):
        return obj.departure_location.location_name if obj.departure_location else None

    def get_arrival_location_name(self, obj):
        return obj.arrival_location.location_name if obj.arrival_location else None

    class Meta:
        model = DrivingSchedule
        fields = [
            'id', 'bus', 'bus_details', 'departure_time', 'arrival_time',
            'departure_location', 'departure_location_name',
            'arrival_location', 'arrival_location_name'
        ]
