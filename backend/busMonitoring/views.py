from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ElectricBus
from .serializers import ElectricBusSerializer

class ElectricBusViewSet(ModelViewSet):
    queryset = ElectricBus.objects.all()
    serializer_class = ElectricBusSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['bus_id', 'status']  # Enable search by these fields
    ordering_fields = ['battery']  # Enable ordering by these fields
