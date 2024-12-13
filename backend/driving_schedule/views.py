# driving_schedule/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import DrivingSchedule
from .serializers import DrivingScheduleSerializer

class DrivingScheduleViewSet(ModelViewSet):
    queryset = DrivingSchedule.objects.all()
    serializer_class = DrivingScheduleSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['bus_id', 'driver_name', 'route_id']
    ordering_fields = ['departure_time', 'arrival_time']
    ordering = ['departure_time']
