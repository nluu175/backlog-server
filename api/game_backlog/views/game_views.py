from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from ..models.Game import Game
from ..serializers import GameSerializer
from ..custom.pagination import GamePagination


# /backlog/games/{game_id}
class GameView(APIView):
    http_method_names = ["get", "put"]

    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)


# /backlog/games
class GamesView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request):
        games = Game.objects.all()

        page = request.query_params.get("page")
        page_size = request.query_params.get("size")

        if page or page_size:
            paginator = GamePagination()
            paginated_games = paginator.paginate_queryset(games, request)
            serializer = GameSerializer(paginated_games, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
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
