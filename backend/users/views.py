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
            token = AccessToken(req.get('token'))
            user_id = token['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "The user that wants to add a user is not found"}, status=status.HTTP_404_NOT_FOUND)
            user_role = user.role  
            required_role = "admin"
            is_valid, message = validate_access_token(req.get('token'), user_role,required_role)
            if is_valid:
                serializer = UserSerializer(data=req)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if not is_valid:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)


class LoginView(APIView):
    def post(self,request):
        print(f"Attempting login with email: {request.data.get('email')} and password: {request.data.get('password')}")
        print(f"data: {request.data}")
        serializer = LoginSerializer(data=request.data)
        user = User.objects.filter(email=request.data.get('email')).first()
        print(f"user: {user.email}")
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                print("success")
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