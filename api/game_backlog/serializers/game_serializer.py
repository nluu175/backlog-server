from rest_framework import serializers
from ..models.Game import Game


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
