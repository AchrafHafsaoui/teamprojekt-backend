from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ElectricBus
from .serializers import ElectricBusSerializer

class ElectricBusViewSet(ModelViewSet):
    queryset = ElectricBus.objects.all()
    serializer_class = ElectricBusSerializer

    def destroy(self, request, *args, **kwargs):
        bus_id = kwargs.get('pk')  # This should match the parameter from the URL

        # Ensure we are using bus_id instead of the database primary key (id)
        bus = get_object_or_404(ElectricBus, bus_id=bus_id)  
        
        bus.delete()
        return Response({"message": "Bus deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
