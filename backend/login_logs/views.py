from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


from users.models import User
from .models import LoginLog
from rest_framework.response import Response
from rest_framework import status
from token_manage.tokens_utils import validate_access_token


class GetLoginLogs(APIView):
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
            required_role = 100
            is_valid, message = validate_access_token(req.get('access'), user_role, required_role)

            if is_valid:
                day_str = req.get('day')
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
            else:
                return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "No access token found"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        req = request.data  
        access = req.get('access')
        refresh = req.get('refresh')
        if not access or not refresh:
            return Response({"error": "tokens must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            access_token  = AccessToken(access)
            user_id = access_token ['user_id']

            refresh_token = RefreshToken(req.get('refresh')) 
            refresh_token.blacklist()

            user = User.objects.get(id=user_id)
            current_time = timezone.now()
            login_log = LoginLog.objects.filter(user=user, session_end__gt=current_time).first()
            if login_log:
                # Update the LoginLog to mark the session as ended
                login_log.session_end = current_time  # Set session_end to the current time
                login_log.logout_reason = "User logged out"
                login_log.save()
                return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
            else: return Response({"message": "could not find the session"}, status=status.HTTP_404_NOT_FOUND)

        except TokenError:
            return Response({"error": "Invalid token2"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found3"}, status=status.HTTP_404_NOT_FOUND)