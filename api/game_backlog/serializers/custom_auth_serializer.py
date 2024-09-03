from rest_framework import serializers
from ..custom.errors import (
    MissingCredentialsError,
    InvalidCredentialsError,
    InactiveUserError,
)
from django.contrib.auth.models import User as DjangoUser


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
