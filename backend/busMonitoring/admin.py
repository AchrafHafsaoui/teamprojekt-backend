from django.contrib import admin
from .models import ElectricBus 


@admin.register(ElectricBus)
class ElectricBusAdmin(admin.ModelAdmin):
    list_display = ("bus_id", "battery", "status", "charging_point")
    search_fields = ("bus_id", "charging_point")


