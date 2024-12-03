from rest_framework.viewsets import ModelViewSet
from .models import ElectricBus
from .serializers import ElectricBusSerializer

class ElectricBusViewSet(ModelViewSet):
    queryset = ElectricBus.objects.all()
    serializer_class = ElectricBusSerializer
