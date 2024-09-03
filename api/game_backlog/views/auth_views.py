from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User as DjangoUser

from ..models.User import User
from ..serializers.user_serializer import UserSerializer
from ..serializers.custom_auth_serializer import LoginSerializer

from rest_framework import status


class LoginView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data["user"]
                token, created = Token.objects.get_or_create(user=user)
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


class SignUpView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            steam_name = serializer.validated_data.get(
                "steam_name", "STEAM_NAME_PLACEHOLDER"
            )
            steam_id = serializer.validated_data.get("steam_id", "STEAM_ID_PLACEHOLDER")
            username = request.data.get("username")
            password = request.data.get("password")

            if not password:
                return Response(
                    {"message": "Password is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if DjangoUser.objects.filter(username=username).exists():
                return Response(
                    {"message": "Username already exists"},
                    status=status.HTTP_409_CONFLICT,
                )

            try:
                django_user = DjangoUser.objects.create_user(
                    username=username, email=email, password=password
                )
                django_user.is_active = False
                django_user.save()

                user = User.objects.create(
                    user=django_user,
                    email=email,
                    steam_name=steam_name,
                    steam_id=steam_id,
                )
                user.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
