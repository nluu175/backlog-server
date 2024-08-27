from rest_framework import serializers
from ..models.Wishlist import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "user",
            "game",
            "order",
            # foreign fields
            "name",
        ]

    def get_name(self, obj):
        return obj.game.name if obj.game else None
