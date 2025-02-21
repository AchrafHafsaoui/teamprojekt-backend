from rest_framework import serializers
from .models import Parking

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id', 'name', 'schema', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']
