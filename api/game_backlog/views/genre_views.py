from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from ..models.Genre import Genre
from ..models.Game import Game

from ..serializers import GenreSerializer


class GenreView(APIView):
    http_method_names = ["get"]

    # NOTE: Currently aiming at hard-coding the genre list (posssibly get from STEAM)
    def get(self, request, genre_id):
        genre = get_object_or_404(Game, id=genre_id)
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenresView(APIView):
    http_method_names = ["get"]

    def get(self, request):
        games = Genre.objects.all()
        serializer = GenreSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
