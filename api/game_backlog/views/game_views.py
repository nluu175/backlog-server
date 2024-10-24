from typing import Optional, Any, Dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpRequest

from ..models.Game import Game
from ..serializers.game_serializer import GameSerializer
from ..custom.pagination import GamePagination


class GameView(APIView):
    """
    API View for handling single game operations.
    Endpoint: /api/games/{game_id}
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request: HttpRequest, game_id: str) -> Response:
        """
        Retrieve a specific game by ID.

        Args:
            request: HTTP request object
            game_id: UUID of the game to retrieve

        Returns:
            Response containing the serialized game data
        """
        game = get_object_or_404(Game, id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GamesView(APIView):
    """
    API View for handling multiple games operations.
    Endpoint: /api/games
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def _handle_pagination(
        self,
        queryset: Any,
        request: HttpRequest,
        page: Optional[str],
        page_size: Optional[str],
    ) -> Response:
        """
        Handle pagination of games queryset if pagination parameters are provided.

        Args:
            queryset: The queryset to paginate
            request: HTTP request object
            page: Page number
            page_size: Number of items per page

        Returns:
            Response with either paginated or full results
        """
        if page or page_size:
            paginator = GamePagination()
            paginated_games = paginator.paginate_queryset(queryset, request)
            serializer = GameSerializer(paginated_games, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _create_game(self, validated_data: Dict[str, Any]) -> Game:
        """
        Create a new game instance from validated data.

        Args:
            validated_data: Validated data from serializer

        Returns:
            Newly created Game instance
        """
        game = Game.objects.create(
            name=validated_data["name"],
            description=validated_data["description"],
            release_date=validated_data["release_date"],
            platform=validated_data["platform"],
            steam_app_id=validated_data["steam_app_id"],
        )

        # Set many-to-many relationship for genres
        game.genres.set(validated_data["genres"])
        return game

    def get(self, request: HttpRequest) -> Response:
        """
        Retrieve all games with optional pagination.

        Args:
            request: HTTP request object with optional page and size query parameters

        Returns:
            Response containing the serialized games data
        """
        games = Game.objects.all()
        page = request.query_params.get("page")
        page_size = request.query_params.get("size")

        return self._handle_pagination(games, request, page, page_size)

    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Create a new game.

        Args:
            request: HTTP request object containing game data

        Returns:
            Response with created game data or validation errors
        """
        serializer = GameSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        game = self._create_game(serializer.validated_data)
        return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)
