from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import LoginLog
from token_manage.tokens_utils import validate_access_token


def get_access_token_from_header(request):
    """Helper function to extract the access token from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]  # Remove 'Bearer ' prefix


class GetLoginLogs(APIView):
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
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        day_str = request.data.get('day')
        if not day_str:
            return Response({"error": "Day parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            day_datetime = datetime.fromisoformat(day_str.replace("Z", "+00:00"))
            day = day_datetime.date()
        except ValueError:
            return Response({"error": "Invalid date format. Use ISO 8601 format (e.g., 2025-02-23T20:23:59.427Z)"}, status=status.HTTP_400_BAD_REQUEST)

        start_of_day = timezone.make_aware(datetime.combine(day, datetime.min.time()))
        end_of_day = start_of_day + timedelta(days=1)

        logs = LoginLog.objects.filter(
            login_at__gte=start_of_day,
            login_at__lt=end_of_day
        ).order_by('-login_at')

        res = [
            {
                "id": log.id,
                "login_at": log.login_at,
                "session_end": log.session_end,
                "logout_reason": log.logout_reason,
                "user_id": log.user_id,
                "user_name": log.user.username
            }
            for log in logs
        ]

        return Response(res, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        access_token = get_access_token_from_header(request)
        refresh_token = request.data.get('refresh')

        if not access_token or not refresh_token:
            return Response({"error": "Access token and refresh token must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = AccessToken(access_token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)

            # Blacklist the refresh token
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            # Update the LoginLog to mark the session as ended
            current_time = timezone.now()
            login_log = LoginLog.objects.filter(user=user, session_end__gt=current_time).first()
            if login_log:
                login_log.session_end = current_time  # Set session_end to the current time
                login_log.logout_reason = "User logged out"
                login_log.save()
                return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Could not find the session"}, status=status.HTTP_404_NOT_FOUND)

        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)