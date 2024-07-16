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
    name = serializers.SerializerMethodField()
    steam_app_id = serializers.SerializerMethodField()

    class Meta:
        model = Backlog
        fields = [
            "id",
            "user",
            "game",
            "status",
            "rating",
            "comment",
            "playtime",
            # foreign fields
            "name",
            "steam_app_id",
        ]

    def get_name(self, obj):
        return obj.game.name if obj.game else None

    def get_steam_app_id(self, obj):
        return obj.game.steam_app_id if obj.game else None
