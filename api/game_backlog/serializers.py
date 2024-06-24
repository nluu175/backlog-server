from rest_framework import serializers

from .models.User import User
from .models.Genre import Genre
from .models.Game import Game
from .models.Backlog import Backlog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "steam_id",
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "id",
            "code",
            "name",
        ]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "description",
            "release_date",
            "genres",
            "platform",
            "steam_app_id",
        ]


class BacklogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backlog
        fields = ["id", "user", "game", "status", "rating", "comment", "playtime"]
