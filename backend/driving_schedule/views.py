from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from token_manage.tokens_utils import validate_access_token
from .models import DrivingSchedule, LocationType
from .serializers import DrivingScheduleSerializer, LocationTypeSerializer


def get_access_token_from_header(request):
    """Helper function to extract the access token from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]  # Remove 'Bearer ' prefix


class LocationTypeViewSet(ModelViewSet):
    queryset = LocationType.objects.all()
    serializer_class = LocationTypeSerializer

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
        # Step 1: Validate token and role for listing location types
        required_role = 20  # Role required to list location types
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Step 1: Validate token and role for retrieving a location type
        required_role = 20  # Role required to retrieve a location type
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Step 1: Validate token and role for creating a location type
        required_role = 50  # Role required to create a location type
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Step 1: Validate token and role for updating a location type
        required_role = 50  # Role required to update a location type
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Step 1: Validate token and role for deleting a location type
        required_role = 50  # Role required to delete a location type
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().destroy(request, *args, **kwargs)


class DrivingScheduleViewSet(ModelViewSet):
    queryset = DrivingSchedule.objects.all()
    serializer_class = DrivingScheduleSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['bus_id', 'driver_name', 'route_id']
    ordering_fields = ['departure_time', 'arrival_time']
    ordering = ['departure_time']

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
        # Step 1: Validate token and role for listing driving schedules
        required_role = 20  # Role required to list driving schedules
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Step 1: Validate token and role for retrieving a driving schedule
        required_role = 20  # Role required to retrieve a driving schedule
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Step 1: Validate token and role for creating a driving schedule
        required_role = 50  # Role required to create a driving schedule
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Step 1: Validate token and role for updating a driving schedule
        required_role = 50  # Role required to update a driving schedule
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Step 1: Validate token and role for deleting a driving schedule
        required_role = 50  # Role required to delete a driving schedule
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().destroy(request, *args, **kwargs)