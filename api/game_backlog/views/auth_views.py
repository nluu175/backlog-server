from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User as DjangoUser

from ..models.User import User
from ..serializers.auth_serializer import LoginSerializer, SignUpSerializer

from rest_framework import status


class LoginView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data["user"]
                # token, created = Token.objects.get_or_create(user=user)
                token = Token.objects.create(user=user)
                data = {"message": "Login successful", "token": token.key}

                return Response(data, status=status.HTTP_200_OK)

        except ValidationError as e:
            # have to get index [0] because error_code is a list
            error_code = e.detail.get("code")[0]

            response_mapping = {
                "inactive_user": Response(
                    {"detail": e.detail.get("detail")}, status=status.HTTP_403_FORBIDDEN
                ),
                "invalid_credentials": Response(
                    {"detail": e.detail.get("detail")},
                    status=status.HTTP_401_UNAUTHORIZED,
                ),
                "missing_credentials": Response(
                    {"detail": e.detail.get("detail")},
                    status=status.HTTP_400_BAD_REQUEST,
                ),
            }

            response_object = response_mapping.get(
                error_code,
                Response(
                    {"detail": "An error occurred"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ),
            )

            return response_object


class LogoutView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        username = request.data.get("username")
        user = DjangoUser.objects.get(username=username)

        # Remove token on logout
        Token.objects.filter(user=user).delete()

        return Response(status=status.HTTP_200_OK)


class SignUpView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data["user"]

            # Django User model
            django_user = DjangoUser.objects.create_user(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            django_user.is_active = False
            django_user.save()

            # My User model
            user = User.objects.create(
                user=django_user,
                email=serializer.validated_data["email"],
                steam_name=serializer.validated_data["steam_name"],
                steam_id=serializer.validated_data["steam_id"],
            )
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            error_code = e.detail.get("code")[0]

            response_mapping = {
                "duplicate_username": Response(
                    {"detail": e.detail.get("detail")},
                    status=status.HTTP_409_CONFLICT,
                ),
                "missing_credentials": Response(
                    {"detail": e.detail.get("detail")},
                    status=status.HTTP_400_BAD_REQUEST,
                ),
                "steam_account_exists": Response(
                    {"detail": e.detail.get("detail")}, status=status.HTTP_409_CONFLICT
                ),
            }

            response_object = response_mapping.get(
                error_code,
                Response(
                    {"detail": "An error occurred"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ),
            )

            return response_object
