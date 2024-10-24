from typing import Dict, Any, Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework import status

from django.contrib.auth.models import User as DjangoUser
from django.db import transaction
from django.http import HttpRequest

from ..models.User import User
from ..serializers.auth_serializer import LoginSerializer, SignUpSerializer


class LoginView(APIView):
    """
    API View for user authentication/login.
    """

    http_method_names = ["post"]

    def _create_success_response(self, user: DjangoUser) -> Response:
        """
        Create success response with new token.

        Args:
            user: Authenticated Django user instance

        Returns:
            Response with token and success message
        """
        token = Token.objects.create(user=user)
        data = {"message": "Login successful", "token": token.key}
        return Response(data, status=status.HTTP_200_OK)

    def _handle_validation_error(self, error: ValidationError) -> Response:
        """
        Handle different types of validation errors.

        Args:
            error: ValidationError instance

        Returns:
            Response with appropriate error message and status code
        """
        error_code = error.detail.get("code", [""])[0]
        error_detail = error.detail.get("detail")

        response_mapping = {
            "inactive_user": (status.HTTP_403_FORBIDDEN, error_detail),
            "invalid_credentials": (status.HTTP_401_UNAUTHORIZED, error_detail),
            "missing_credentials": (status.HTTP_400_BAD_REQUEST, error_detail),
        }

        status_code, detail = response_mapping.get(
            error_code, (status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred")
        )

        return Response({"detail": detail}, status=status_code)

    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Handle login request.

        Args:
            request: HTTP request with login credentials

        Returns:
            Response with token or error message
        """
        serializer = LoginSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return self._create_success_response(serializer.validated_data["user"])
        except ValidationError as e:
            return self._handle_validation_error(e)


class LogoutView(APIView):
    """
    API View for user logout.
    """

    http_method_names = ["post"]

    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Handle logout request.

        Args:
            request: HTTP request with username

        Returns:
            Empty response with success status
        """
        username = request.data.get("username")
        user = DjangoUser.objects.get(username=username)
        Token.objects.filter(user=user).delete()
        return Response(status=status.HTTP_200_OK)


class SignUpView(APIView):
    """
    API View for user registration.
    """

    http_method_names = ["post"]

    def _create_django_user(self, validated_data: Dict[str, Any]) -> DjangoUser:
        """
        Create a new Django user instance.

        Args:
            validated_data: Validated data from serializer

        Returns:
            New Django user instance
        """
        django_user = DjangoUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        django_user.is_active = False
        django_user.save()
        return django_user

    def _create_custom_user(
        self, django_user: DjangoUser, validated_data: Dict[str, Any]
    ) -> User:
        """
        Create a new custom user instance.

        Args:
            django_user: Associated Django user instance
            validated_data: Validated data from serializer

        Returns:
            New custom User instance
        """
        user = User.objects.create(
            user=django_user,
            email=validated_data["email"],
            steam_name=validated_data["steam_name"],
            steam_id=validated_data["steam_id"],
        )
        user.save()
        return user

    def _handle_validation_error(self, error: ValidationError) -> Response:
        """
        Handle different types of validation errors.

        Args:
            error: ValidationError instance

        Returns:
            Response with appropriate error message and status code
        """
        error_code = error.detail.get("code", [""])[0]
        error_detail = error.detail.get("detail")

        response_mapping = {
            "duplicate_username": (status.HTTP_409_CONFLICT, error_detail),
            "missing_credentials": (status.HTTP_400_BAD_REQUEST, error_detail),
            "steam_account_exists": (status.HTTP_409_CONFLICT, error_detail),
        }

        status_code, detail = response_mapping.get(
            error_code,
            (
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred. Please try again.",
            ),
        )

        return Response({"detail": detail}, status=status_code)

    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Handle sign-up request.

        Args:
            request: HTTP request with user registration data

        Returns:
            Response with created user data or error message
        """
        serializer = SignUpSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            django_user = self._create_django_user(serializer.validated_data)
            self._create_custom_user(django_user, serializer.validated_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return self._handle_validation_error(e)
