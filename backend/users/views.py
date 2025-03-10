import jwt
from login_logs.utils import create_login_log
from token_manage.tokens_utils import validate_access_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, LoginSerializer
from .models import User

def get_access_token_from_header(request):
    """Helper function to extract the access token from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]  # Remove 'Bearer ' prefix


class GetUsersView(APIView):
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
        required_role = 100
        is_valid, message = validate_access_token(access_token, user_role, required_role)
        if is_valid:
            users = User.objects.all()
            user_data = [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
                for user in users
            ]
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)



class AddUserView(APIView):
    def post(self, request):
            access_token = get_access_token_from_header(request)
            if not access_token:
                return Response({"error": "Authorization header with Bearer token is required"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                token = AccessToken(access_token)
                user_id = token['user_id']
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "The user that wants to add a user is not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            user_role = user.role
            required_role = 100
            is_valid, message = validate_access_token(access_token, user_role, required_role)
            if is_valid:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({
                        'id': user.id,
                        'username': user.email,
                        'email': user.email,
                        'role': user.role,
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                create_login_log(user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=401)
        return Response({"error": "Credentials missing"}, status=401)
                

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
        access_token = get_access_token_from_header(request)
        print(access_token)
        if not access_token:
            return Response({"detail": "Authorization header with Bearer token is required"}, status=status.HTTP_400_BAD_REQUEST)

        min_required_role = request.data.get('role')
        if not min_required_role:
            return Response({"detail": "Role is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = AccessToken(access_token)
            user_id = payload['user_id']
            if not user_id:
                raise AuthenticationFailed("Invalid token: User ID not found")

            user = User.objects.get(id=user_id)
            user_role = user.role
            is_valid, message = validate_access_token(access_token, user_role, int(min_required_role))

            if not is_valid:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
            return Response({"message": "Authorized access"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UpdateInfo(APIView):
    def post(self, request):
        access_token = get_access_token_from_header(request)
        if not access_token:
            return Response({"detail": "Authorization header with Bearer token is required"}, status=status.HTTP_400_BAD_REQUEST)

        new_email = request.data.get('newEmail')
        new_username = request.data.get('newUserName')
        new_password = request.data.get('newPwd')
        old_password = request.data.get('oldPwd')

        if not old_password:
            return Response({"detail": "Old password is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_email and not new_username and not new_password:
            return Response({"detail": "At least one attribute must be provided for update"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = AccessToken(access_token)
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)

            if not user.check_password(old_password):
                return Response({"detail": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)

            if new_email:
                user.email = new_email
            if new_username:
                user.username = new_username
            if new_password:
                user.set_password(new_password)

            user.save()
            return Response({"detail": "User information updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UpdateRole(APIView):
    def post(self, request):
        access_token = get_access_token_from_header(request)
        if not access_token:
            return Response({"error": "Authorization header with Bearer token is required"}, status=status.HTTP_401_UNAUTHORIZED)

        member_id = request.data.get('member_id')
        new_role = request.data.get('new_role')

        if not member_id or not new_role:
            return Response({"detail": "Member ID and new role are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = AccessToken(access_token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "The user that wants to update the role is not found"}, status=status.HTTP_404_NOT_FOUND)

        user_role = user.role
        required_role = 100
        is_valid, message = validate_access_token(access_token, user_role, required_role)
        if is_valid:
            try:
                member = User.objects.get(id=member_id)
                member.role = new_role
                member.save()
                return Response({"detail": f"User {member.username}'s role updated successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "The user to be updated was not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)