from rest_framework import serializers
from ..custom.errors import (
    MissingCredentialsError,
    InvalidCredentialsError,
    InactiveUserError,
    UsernameAlreadyExistsError,
    SteamAccountAlreadyExistsError,
)
from django.contrib.auth.models import User as DjangoUser
from ..models.User import User


class LoginSerializer(serializers.Serializer):
    # have to set required to False to use the custom error messages (MissingCredentialsError)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise MissingCredentialsError()

        user = DjangoUser.objects.get(username=username)

        # use check_password() instead of authenticate() as the latter will return None if the user is inactive, leading toe InvalidCredentialsError being raised
        if not user.check_password(password):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InactiveUserError()

        data["user"] = user
        return data


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    steam_name = serializers.CharField()
    steam_id = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        steam_name = data.get("steam_name")
        steam_id = data.get("steam_id")

        for key in [email, username, password, steam_name, steam_id]:
            if not key:
                raise MissingCredentialsError()

        user = DjangoUser.objects.filter(username=username).exists()
        if user:
            raise UsernameAlreadyExistsError()

        steam_name_exists = User.objects.filter(steam_name=steam_name).exists()
        steam_id_exists = User.objects.filter(steam_id=steam_id).exists()
        if steam_name_exists or steam_id_exists:
            raise SteamAccountAlreadyExistsError()

        # data["user"] = user
        return data
