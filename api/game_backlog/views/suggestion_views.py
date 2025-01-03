from django.http import HttpRequest
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import ast

from ..models.Backlog import Backlog
from ..models.SuggestionGame import SuggestionGame
from ..models.User import User
from ..services.genai_service import GenAIService
from ..utils.response_processor import process_genai_response


class SuggestionByGenreView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.genai_service = GenAIService()

    def _parse_genre_param(self, game_genre: str) -> str:
        """Parse and validate the game_genre parameter."""
        return

    def _parse_refresh_param(self, refresh: str) -> bool:
        """Parse and validate the refresh parameter."""
        if not refresh:
            return False

        refresh = refresh.lower()
        if refresh not in ["true", "false"]:
            raise ValueError("Refresh parameter must be 'true' or 'false'")

        return refresh == "true"

    def _get_cached_suggestion(self, user: User, genre: str) -> Response:
        # get the latest one from the list
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
            # Get game list from user's backlog
            # NOTE: Only get games of the input genres to reduce the amount of input to Gemini API
            game_list = list(
                Backlog.objects.select_related("game")
                .filter(game__genres__code__icontains=genre)
                # .values_list("game__name", "game__steam_app_id")
                .values_list("game__steam_app_id")
                .distinct()
            )

            # Generate suggestions
            genai_response = self.genai_service.generate_game_suggestions(
                genre_prompt=genre, game_list=game_list
            )

            # Process response
            # Clean up response from Gemini
            processed_games = process_genai_response(genai_response.text)
            game_ids = [game[0] for game in processed_games]

            # Cache suggestion
            SuggestionGame.objects.create(
                suggestion_type=SuggestionGame.SuggestionTypes.BY_GENRE,
                user=user,
                game_list=" ".join(map(str, game_ids)),
            )

            return Response(
                {
                    "game_genre": genre,
                    "game_list": game_list,
                    "suggested_games": processed_games,
                }
            )  # game list
            # return Response({"game_genre": genre, "game_list": game_ids}) # final

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Get game suggestions based on genre. Currently only supports game suggestion by genre

        Args:
            game_genre (str): Genre to base suggestions on. This should be in the list of the genres in our database (Genre)
            refresh (bool): Whether to generate new suggestions or use cached ones
        """
        try:
            # Get and validate parameters
            user = User.objects.get(user=request.user)
            genre = request.query_params.get("game_genre")
            refresh = self._parse_refresh_param(request.query_params.get("refresh"))

            # Return new suggestions if refresh is True else returns cache
            if refresh:
                return self._generate_new_suggestion(user, genre)
            return self._get_cached_suggestion(user, genre)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
