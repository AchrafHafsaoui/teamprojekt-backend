from datetime import datetime, timezone
from rest_framework_simplejwt.tokens import AccessToken

def validate_access_token(access_token: str, user_role: str, required_role: str):
    """
    Validates the access token and checks if the user's role matches the required role.

    Args:
        access_token (str): The JWT access token to validate.
        user_role (str): The role of the token owner.
        required_role (str): The role required to access the endpoint.

    Returns:
        tuple: A boolean indicating access and a rejection message if any.
    """
    if access_token != None:
        try:
            token = AccessToken(access_token)
            exp_time = token.get("exp", None)
            if exp_time is not None:
                exp_datetime = datetime.fromtimestamp(exp_time, tz=timezone.utc)
                if exp_datetime < token.current_time:
                    return False, "Access token has expired"

                if user_role < required_role:
                    return False, f"Access denied: user role is lower than required role"

                if user_role >= required_role and exp_datetime > token.current_time:
                    return True, "Access granted"
            else: return False, f"Invalid token: {str(e)}"

        except Exception as e:
            return False, f"Invalid token: {str(e)}"
    else: return False, f"token required"
