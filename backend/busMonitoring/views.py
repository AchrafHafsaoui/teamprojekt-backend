from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from token_manage.tokens_utils import validate_access_token
from .models import ElectricBus
from .serializers import ElectricBusSerializer


def get_access_token_from_header(request):
    """Helper function to extract the access token from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]  # Remove 'Bearer ' prefix


class ElectricBusViewSet(ModelViewSet):
    queryset = ElectricBus.objects.all()
    serializer_class = ElectricBusSerializer

    def _validate_token_and_role(self, request, required_role):
        """Helper function to validate the token and user role."""
        access_token = get_access_token_from_header(request)
        if not access_token:
            return Response({"error": "Authorization header with Bearer token is required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = AccessToken(access_token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "The user is not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user_role = user.role
        is_valid, message = validate_access_token(access_token, user_role, required_role)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        return None  # No error, validation passed

    def list(self, request, *args, **kwargs):
        required_role = 20
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        required_role = 20 
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        required_role = 50 
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        required_role = 50
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        required_role = 50  
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        bus_id = kwargs.get('pk')

        bus = get_object_or_404(ElectricBus, bus_id=bus_id)

        bus.delete()
        return Response({"message": "Bus deleted successfully"}, status=status.HTTP_204_NO_CONTENT)