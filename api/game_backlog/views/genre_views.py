from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpRequest

from ..models.Genre import Genre
from ..models.Game import Game
from ..serializers.genre_serializer import GenreSerializer


class GenreView(APIView):
    """
    API View for handling single genre operations.
    Endpoint: /api/genres/{genre_id}

    Note: Currently aiming at hard-coding the genre list (https://steamdb.info/tags/#genreAM)
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request: HttpRequest, genre_id: str) -> Response:
        """
        Retrieve a specific genre by ID.

        Args:
            request: HTTP request object
            genre_id: UUID of the genre to retrieve

        Returns:
            Response containing the serialized genre data
        """
        genre = get_object_or_404(Game, id=genre_id)
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenresView(APIView):
    """
    API View for handling multiple genres operations.
    Endpoint: /api/genres
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request: HttpRequest) -> Response:
        """
        Retrieve all genres.

        Args:
            request: HTTP request object

        Returns:
            Response containing the serialized genres data
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
