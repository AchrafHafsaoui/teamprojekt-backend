from rest_framework import serializers
from .models import ElectricBus

class ElectricBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricBus
        fields = '__all__'
