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


class GetUsersView(APIView):
    def post(self,request):
        if request.method == 'POST':
            req = request.data
            if req.get('access'):
                token = AccessToken(req.get('access'))
                print(f"Access Token: {req.get('access')}")
                user_id = token['user_id']
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({"error": "The user is not found"}, status=status.HTTP_404_NOT_FOUND)
                user_role = user.role  
                required_role = 100
                accessToken = req.get('access')
                is_valid, message = validate_access_token(accessToken, user_role,required_role)
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
            else: return Response({"error": "no access token found"}, status=status.HTTP_401_UNAUTHORIZED)



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
            is_valid, message = validate_access_token(req.get('access'), user_role,required_role)
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
                create_login_log(user)
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
        min_required_role = request.data.get('role')
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
        

class UpdateInfo(APIView):
    def post(self, request):
        access_token = request.data.get('access')
        newEmail= request.data.get('newEmail')
        newUserName= request.data.get('newUserName')
        newPwd= request.data.get('newPwd')
        oldPwd= request.data.get('oldPwd')

        if not access_token or not oldPwd:
            return Response(
                {"detail": "Access token and old password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not newEmail and not newUserName and not newPwd:
            return Response(
                {"detail": "At least one attribute must be provided for update"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payload = AccessToken(access_token)
            user_id = payload['user_id']
            
            if not user_id:
                return Response(
                    {"detail": "Invalid token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Fetch the user from the database
            user = User.objects.get(id=user_id)

            # Check if the old password is correct
            if not user.check_password(oldPwd):
                return Response(
                    {"detail": "Incorrect old password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update fields if they are provided
            if newEmail:
                user.email = newEmail
            if newUserName:
                user.username = newUserName
            if newPwd:
                user.set_password(newPwd)

            # Save changes
            user.save()

            return Response(
                {"detail": "User information updated successfully"},
                status=status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"detail": "Token has expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.DecodeError:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        

class UpdateRole(APIView):
    def post(self, request):
        access_token = request.data.get('access')
        member_id= request.data.get('member_id')
        new_role= request.data.get('new_role')

        if not access_token or not member_id or not new_role:
            return Response(
                {"detail": "Access token, member_id and role are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = AccessToken(access_token)
        user_id = token['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "The user that wants to add a user is not found"}, status=status.HTTP_404_NOT_FOUND)
        user_role = user.role  
        required_role = 100
        is_valid, message = validate_access_token(access_token, user_role,required_role)
        if is_valid:
            try:
                member = User.objects.get(id=member_id)

                member.role = new_role
                member.save()

                return Response(
                    {"detail": f"User {member.username}'s role updated successfully"},
                    status=status.HTTP_200_OK,
                )

            except User.DoesNotExist:
                return Response(
                    {"error": "The user to be updated was not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)