from django.contrib import admin
from .models import ElectricBus

@admin.register(ElectricBus)
class ElectricBusAdmin(admin.ModelAdmin):
    list_display = ("bus_id", "vehicle_type", "battery", "status", "charging_location")
    search_fields = ("bus_id", "vehicle_type", "charging_location")
