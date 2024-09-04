from rest_framework.exceptions import ValidationError


class MissingCredentialsError(ValidationError):
    default_detail = {
        "detail": "Username and password are required.",
        "code": "missing_credentials",
    }


class InvalidCredentialsError(ValidationError):
    default_detail = {
        "detail": "Invalid credentials. Please try again.",
        "code": "invalid_credentials",
    }


class InactiveUserError(ValidationError):
    default_detail = {"detail": "User account is not active.", "code": "inactive_user"}


class UsernameAlreadyExistsError(ValidationError):
    default_detail = {
        "detail": "Username already exists.",
        "code": "duplicate_username",
    }


class SteamAccountAlreadyExistsError(ValidationError):
    default_detail = {
        "detail": "Steam account already exists.",
        "code": "duplicate_steam_account",
    }


# from rest_framework.exceptions import APIException
# from rest_framework import status

# --- API Exception Classes ---
# # Custom Exceptions Classes
# class UserNotActiveException(APIException):
#     status_code = status.HTTP_403_FORBIDDEN
#     default_detail = "User account is not active."


# class InvalidCredentialsException(APIException):
#     status_code = status.HTTP_401_UNAUTHORIZED
#     default_detail = "Invalid credentials. Please try again."


# class MissingCredentialsException(APIException):
#     status_code = status.HTTP_400_BAD_REQUEST
#     default_detail = "Username and password are required."
