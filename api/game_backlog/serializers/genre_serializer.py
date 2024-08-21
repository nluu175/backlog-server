from rest_framework import serializers
from ..models.Genre import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "id",
            "code",
            "name",
        ]
