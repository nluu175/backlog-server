from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from ..models.Game import Game
from ..serializers import GameSerializer


class GameView(APIView):
    http_method_names = ["get"]

    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GamesView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GameSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data["name"]
            description = serializer.validated_data["description"]
            release_date = serializer.validated_data["release_date"]

            # genres is a list of genre's code
            genres = serializer.validated_data["genres"]
            platform = serializer.validated_data["platform"]
            steam_app_id = serializer.validated_data["steam_app_id"]

            game = Game.objects.create(
                name=name,
                description=description,
                release_date=release_date,
                platform=platform,
                steam_app_id=steam_app_id,
            )

            game.genres.set(genres)

            return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
