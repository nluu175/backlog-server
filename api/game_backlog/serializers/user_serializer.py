from rest_framework import serializers
from ..models.User import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "steam_name",
            "steam_id",
        ]
