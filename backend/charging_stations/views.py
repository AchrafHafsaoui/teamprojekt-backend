from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Station
from .serializers import StationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class StationList(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['station_id', 'availability']  # Enable search by these fields
    ordering_fields = ['charging_power']  # Enable ordering by these fields


@api_view(['POST'])
def add_charging_station(request):
    serializer = StationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


