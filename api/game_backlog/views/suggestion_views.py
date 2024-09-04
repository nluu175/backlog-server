from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db import transaction

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

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        game_genre_request = request.query_params.get("game_genre_request", None)
        if not game_genre_request:
            return Response(
                {"error": "No game_genre_request parameter provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        game_data = list(
            Backlog.objects.select_related("game").values_list(
                "game__name", "game__steam_app_id", flat=False
            )
        )

        try:
            genai_response = self.genai_service.generate_game_suggestions(
                genre_prompt=game_genre_request,
                game_list=game_data,
            )
            games_list_processed = process_genai_response(genai_response.text)

            game_id_list = [game_item[1] for game_item in games_list_processed]

            # TODO: REFACTOR THIS INTO A SERVICE
            SuggestionGame.objects.create(
                suggestion_type=SuggestionGame.SuggestionTypes.BY_GENRE,
                user=User.objects.get(user=request.user),
                game_list=" ".join(str(x) for x in game_id_list),
            )

            response = {
                "game_genre": game_genre_request,
                "game_list": games_list_processed,
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
