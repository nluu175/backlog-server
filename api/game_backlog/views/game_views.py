from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction

from ..models.Game import Game
from ..serializers.game_serializer import GameSerializer
from ..custom.pagination import GamePagination


# /api/games/{game_id}
class GameView(APIView):
    # The view will only allow requests from users who provide a valid authentication token.
    # Only authenticated users (those with a valid token) will be permitted to interact with the view.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    http_method_names = ["get"]

    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)


# /api/games
class GamesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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

    @transaction.atomic
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
