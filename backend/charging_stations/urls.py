from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationList , add_charging_station

router = DefaultRouter()
router.register(r'stations',StationList,basename="stations")

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/charging-stations/', add_charging_station, name='add_charging_station'),
]
