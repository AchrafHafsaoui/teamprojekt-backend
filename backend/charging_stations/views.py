from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Station
from .serializers import StationSerializer

class StationList(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['station_id', 'availability']  # Enable search by these fields
    ordering_fields = ['charging_power']  # Enable ordering by these fields
