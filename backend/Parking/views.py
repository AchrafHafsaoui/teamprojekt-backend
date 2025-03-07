from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import ParkingSerializer
from .models import Parking
from users.models import User
from token_manage.tokens_utils import validate_access_token


def get_access_token_from_header(request):
    """Helper function to extract the access token from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]  # Remove 'Bearer ' prefix


class CreateNewParking(APIView):
    def post(self, request):
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
        required_role = 50
        is_valid, message = validate_access_token(access_token, user_role, required_role)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        schema = request.data.get('schema')

        if not name:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the parking name already exists
        if Parking.objects.filter(name=name).exists():
            return Response({"error": "A parking with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new parking object
        parking = Parking.objects.create(
            name=name,
            schema=schema if schema else "",
            created_by=user
        )

        # Serialize the created object
        serializer = ParkingSerializer(parking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetAllParkings(APIView):
    serializer_class = ParkingSerializer

    def post(self, request):
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
        required_role = 0
        is_valid, message = validate_access_token(access_token, user_role, required_role)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        # Fetch all parkings
        parkings = Parking.objects.all()

        # Serialize the data
        serializer = ParkingSerializer(parkings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditParking(APIView):
    def post(self, request):
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
        required_role = 50
        is_valid, message = validate_access_token(access_token, user_role, required_role)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        # Extract parking id, name, and schema from request
        parking_id = request.data.get('parking_id')
        new_name = request.data.get('newName')
        new_schema = request.data.get('newSchema')

        if not parking_id:
            return Response({"error": "Parking ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parking = Parking.objects.get(id=parking_id)
        except Parking.DoesNotExist:
            return Response({"error": "Parking not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the new parking name is unique
        if new_name and Parking.objects.filter(name=new_name).exclude(id=parking_id).exists():
            return Response({"error": "A parking with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the parking object with new data
        if new_name:
            parking.name = new_name
        if new_schema:
            parking.schema = new_schema

        parking.save()

        serializer = ParkingSerializer(parking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveParking(APIView):
    def post(self, request):
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
        required_role = 50
        is_valid, message = validate_access_token(access_token, user_role, required_role)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        parking_id = request.data.get('parking_id')
        if not parking_id:
            return Response({"error": "Parking ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parking = Parking.objects.get(id=parking_id)
            parking.delete()
            return Response({"message": "Parking deleted successfully"}, status=status.HTTP_200_OK)
        except Parking.DoesNotExist:
            return Response({"error": "Parking not found"}, status=status.HTTP_404_NOT_FOUND)