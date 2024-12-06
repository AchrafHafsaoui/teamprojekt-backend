from django.contrib import admin
from .models import Station

@admin.register(Station)    
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'availability', 'charging_power', 'max_power', 'updated_at')
    search_fields = ('station_id',)
