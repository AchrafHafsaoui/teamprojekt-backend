import jwt
from token_manage.tokens_utils import validate_access_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, LoginSerializer
from .models import User


class AddUserView(APIView):
    def post(self,request):
        if request.method == 'POST':
            req = request.data
            token = AccessToken(req.get('access'))
            user_id = token['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "The user that wants to add a user is not found"}, status=status.HTTP_404_NOT_FOUND)
            user_role = user.role  
            required_role = 100
            is_valid, message = validate_access_token(req.get('token'), user_role,required_role)
            if is_valid:
                serializer = UserSerializer(data=req)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({
                        'id': user.id,
                        'username': user.email,
                        'email': user.email,
                        'role': user.role,
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if not is_valid:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)


class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        user = User.objects.filter(email=request.data.get('email')).first()
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                print(f"role: {user.role}")
                refresh = RefreshToken.for_user(user)
                return Response({
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=401)
        return Response({"error": "creds missing"}, status=401)
                

class RefreshAccessTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            
            access_token = str(refresh.access_token)

            return Response({
                "access": access_token
            }, status=status.HTTP_200_OK)

        except Exception as e:
            raise AuthenticationFailed("Invalid or expired refresh token")
        

class IsAuthView(APIView):
    def post(self, request):
        access_token = request.data.get('access')
        print(f"Access Token: {access_token}")
        min_required_role = request.data.get('role')
        print(f"min_required_role: {min_required_role}")
        if not access_token or not min_required_role:
            return Response(
                {"detail": "Access token and role are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            payload = AccessToken(access_token)
            user_id = payload['user_id']
            if not user_id:
                raise AuthenticationFailed("Invalid token: User ID not found")
                
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            user_role = user.role
            is_valid, message = validate_access_token(access_token, user_role, int(min_required_role))
            
            if not is_valid:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
            return Response({"message": "Authorized access"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)