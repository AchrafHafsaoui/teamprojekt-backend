from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from token_manage.tokens_utils import validate_access_token
from .models import Station
from .serializers import StationSerializer


def get_access_token_from_header(request):
    """Helper function to extract the access token from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]  # Remove 'Bearer ' prefix


class StationList(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['station_id', 'availability']  # Enable search by these fields
    ordering_fields = ['charging_power']  # Enable ordering by these fields

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
        # Step 1: Validate token and role for listing stations
        required_role = 20  # Role required to list stations
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Step 1: Validate token and role for retrieving a single station
        required_role = 20  # Role required to retrieve a station
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Step 1: Validate token and role for creating a station
        required_role = 50  # Role required to create a station
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Step 1: Validate token and role for updating a station
        required_role = 50  # Role required to update a station
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Step 1: Validate token and role for deleting a station
        required_role = 50  # Role required to delete a station
        validation_response = self._validate_token_and_role(request, required_role)
        if validation_response:
            return validation_response

        # Step 2: Proceed with the original logic
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
def add_charging_station(request):
    # Step 1: Validate token and role
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
    required_role = 50  # Role required to add a charging station
    is_valid, message = validate_access_token(access_token, user_role, required_role)
    if not is_valid:
        return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

    # Step 2: Proceed with the original logic
    data = request.data.copy()  # Create a mutable copy of request data
    serializer = StationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)