from django.utils import timezone
from login_logs.models import LoginLog

def create_login_log(user):
    """
    Creates a LoginLog entry for the given user.
    If there is an active session (session_end > current time), it ends that session first.
    """
    current_time = timezone.now()
    active_sessions = LoginLog.objects.filter(user=user, session_end__gt=current_time)

    for session in active_sessions:
        session.session_end = current_time
        session.logout_reason = "Session ended by new login" 
        session.save()

    login_log = LoginLog.objects.create(
        user=user,
        login_at=current_time,
    )

    return login_log