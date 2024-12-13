from token_manage.tokens_utils import validate_access_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User  # Import your User model

class SomeProtectedView(APIView):
    def get(self, request):
        # Extract the token from the request (assuming it's passed in the body, adjust if it's in headers)
        access_token = request.data.get('access')
        
        if not access_token:
            return Response({"error": "Access token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the token to extract the user_id
            token = AccessToken(access_token)
            user_id = token['user_id']  # Assuming the token has 'user_id' claim

            # Get the user from the database using the extracted user_id
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Now you have the user's role, and you can check it
            user_role = user.role  # Adjust this based on how the 'role' is stored in your User model
            required_role = "admin"

            # Validate token and role
            is_valid, message = validate_access_token(access_token, user_role, required_role)

            if not is_valid:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

            # Logic for authorized access
            return Response({"message": "Authorized access"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
