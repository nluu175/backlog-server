from rest_framework import serializers
from ..models.Backlog import Backlog


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
