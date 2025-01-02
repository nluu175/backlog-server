from django.http import HttpRequest
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models.Backlog import Backlog
from ..models.SuggestionGame import SuggestionGame
from ..models.User import User
from ..services.genai_service import GenAIService
from ..utils.response_processor import process_genai_response


class SuggestionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.genai_service = GenAIService()

    def _parse_refresh_param(self, refresh_param: str) -> bool:
        """Parse and validate the refresh parameter."""
        if not refresh_param:
            return False

        refresh_param = refresh_param.lower()
        if refresh_param not in ["true", "false"]:
            raise ValueError("Refresh parameter must be 'true' or 'false'")

        return refresh_param == "true"

    def _get_cached_suggestion(self, user: User, genre: str) -> Response:
        suggestion = (
            SuggestionGame.objects.filter(
                suggestion_type=SuggestionGame.SuggestionTypes.BY_GENRE, user=user
            )
            .order_by("created_at")
            .first()
        )

        if not suggestion:
            return Response(
                {"error": "No suggestion found. Please set refresh=true"},
                status=status.HTTP_404_NOT_FOUND,
            )

        game_list = [int(game_id) for game_id in suggestion.game_list.split()]
        return Response({"game_genre": genre, "game_list": game_list})

    def _generate_new_suggestion(self, user: User, genre: str) -> Response:
        """Generate new game suggestions using GenAI."""
        if not genre:
            return Response(
                {"error": "game_genre_request parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get game data
            game_data = list(
                Backlog.objects.select_related("game").values_list(
                    "game__name", "game__steam_app_id"
                )
            )

            # Generate suggestions
            genai_response = self.genai_service.generate_game_suggestions(
                genre_prompt=genre, game_list=game_data
            )

            # Process response
            processed_games = process_genai_response(genai_response.text)
            game_ids = [game[1] for game in processed_games]

            # Cache suggestion
            SuggestionGame.objects.create(
                suggestion_type=SuggestionGame.SuggestionTypes.BY_GENRE,
                user=user,
                game_list=" ".join(map(str, game_ids)),
            )

            return Response({"game_genre": genre, "game_list": game_ids})

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Get game suggestions based on genre.

        Query Parameters:
            game_genre_request (str): Genre to base suggestions on
            refresh (bool): Whether to generate new suggestions or use cached ones
        """
        try:
            # Get and validate parameters
            genre = request.query_params.get("game_genre_request")
            refresh = self._parse_refresh_param(request.query_params.get("refresh"))
            user = User.objects.get(user=request.user)

            # Return cached or new suggestions
            if refresh:
                return self._generate_new_suggestion(user, genre)
            return self._get_cached_suggestion(user, genre)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
