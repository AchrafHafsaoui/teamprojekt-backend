from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import ParkingSerializer
from .models import Parking
from users.models import User
from rest_framework.response import Response
from rest_framework import status
from token_manage.tokens_utils import validate_access_token




class CreateNewParking(APIView):
    def post(self,request):
        if request.method == 'POST':
            req = request.data 
            if req.get('access'):
                token = AccessToken(req.get('access'))
                user_id = token['user_id']
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({"error": "The user is not found"}, status=status.HTTP_404_NOT_FOUND)
                user_role = user.role  
                required_role = 50
                is_valid, message = validate_access_token(req.get('access'), user_role,required_role)
                if is_valid:
                    name = req.get('name')
                    schema = req.get('schema')

                    if not name:
                        return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

                    # Check if the parking name already exists
                    if Parking.objects.filter(name=name).exists():
                        return Response({"error": "A parking with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

                    # Create the new parking object
                    if(schema):
                        parking = Parking.objects.create(
                            name=name,
                            schema=schema,
                            created_by=user
                        )
                    else: 
                        parking = Parking.objects.create(
                            name=name,
                            schema="",
                            created_by=user
                        )
                    

                    # Serialize the created object
                    serializer = ParkingSerializer(parking)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
            else: return Response({"error": "no access token found"}, status=status.HTTP_401_UNAUTHORIZED)

class GetAllParkings(APIView):
    serializer_class = ParkingSerializer
    def post(self, request):
        req = request.data  
        if req.get('access'):
            token = AccessToken(req.get('access'))
            user_id = token['user_id']

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "The user is not found"}, status=status.HTTP_404_NOT_FOUND)

            user_role = user.role  
            required_role = 0
            is_valid, message = validate_access_token(req.get('access'), user_role, required_role)

            if is_valid:
                # Fetch all parkings created by the authenticated user
                parkings = Parking.objects.filter(created_by=user)

                # Serialize the data
                serializer = ParkingSerializer(parkings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "No access token found"}, status=status.HTTP_401_UNAUTHORIZED)
        

class EditParking(APIView):
    def post(self,request):
        if request.method == 'POST':
            req = request.data 
            if req.get('access'):
                token = AccessToken(req.get('access'))
                user_id = token['user_id']
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({"error": "The user is not found"}, status=status.HTTP_404_NOT_FOUND)
                user_role = user.role  
                required_role = 50
                is_valid, message = validate_access_token(req.get('access'), user_role,required_role)
                if is_valid:
                    # Extract parking id, name, and schema from request
                    parking_id = req.get('parking_id')
                    newName = req.get('newName')
                    newSchema = req.get('newSchema')

                    if not parking_id:
                        return Response({"error": "Parking ID is required"}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        parking = Parking.objects.get(id=parking_id)
                    except Parking.DoesNotExist:
                        return Response({"error": "Parking not found"}, status=status.HTTP_404_NOT_FOUND)

                    # Check if the new parking name is unique
                    if newName and Parking.objects.filter(name=newName).exclude(id=parking_id).exists():
                        return Response({"error": "A parking with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

                    # Update the parking object with new data
                    if newName:
                        parking.name = newName
                    if newSchema:
                        parking.schema = newSchema
                    
                    parking.save()

                    serializer = ParkingSerializer(parking)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
            else: return Response({"error": "no access token found"}, status=status.HTTP_401_UNAUTHORIZED)

class RemoveParking(APIView):
    def post(self,request):
        if request.method == 'POST':
            req = request.data 
            if req.get('access'):
                token = AccessToken(req.get('access'))
                user_id = token['user_id']
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({"error": "The user is not found"}, status=status.HTTP_404_NOT_FOUND)
                user_role = user.role  
                required_role = 50
                is_valid, message = validate_access_token(req.get('access'), user_role,required_role)
                if is_valid:
                    parking_id = req.get('parking_id')

                    if not parking_id:
                        return Response({"error": "Parking ID is required"}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        parking = Parking.objects.get(id=parking_id)
                        
                        parking.delete()
                        
                        return Response({"message": "Parking deleted successfully"}, status=status.HTTP_200_OK)
                    except Parking.DoesNotExist:
                        return Response({"error": "Parking not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
            else: return Response({"error": "no access token found"}, status=status.HTTP_401_UNAUTHORIZED)