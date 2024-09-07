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

    @transaction.atomic
    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Cache the result of the suggestion in GameSuggestion database.
        Will automatically refresh the cache if the user WANTS to. This can be done by passing a refresh (Boolean) param.
        Currently accepts params:
            - game_genre_request (string), later will be the genre of the game (must match the genre in the database)
            - refresh (boolean): refetch the suggestion from the model (default: false)
        """
        game_genre_request = request.query_params.get("game_genre_request", None)
        refresh = request.query_params.get("refresh")
        if refresh.lower() == "true":
            refresh = True
        elif refresh.lower() == "false":
            refresh = False
        else:
            # TODO: RAISE error here
            refresh = None

        if refresh is False:  # refresh = True
            suggestion_game_object = (
                SuggestionGame.objects.filter(
                    suggestion_type=SuggestionGame.SuggestionTypes.BY_GENRE,
                    user=User.objects.get(user=request.user),
                )
                .order_by(
                    "created_at",  #  a `-` before column name mean "descending order", while without - mean "ascending".
                )
                .first()
            )

            # TODO: No previous record found
            if not suggestion_game_object:
                return Response(
                    {"error": "No suggestion found. Must set `refresh` to False"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            else:
                game_list_to_int = [
                    int(game_id)
                    for game_id in suggestion_game_object.game_list.split(" ")
                ]
                return Response(
                    {
                        "game_genre": game_genre_request,
                        "game_list": game_list_to_int,
                    }
                )
        else:
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

                # game_name_list = [game_item[0] for game_item in games_list_processed]
                game_id_list = [game_item[1] for game_item in games_list_processed]

                SuggestionGame.objects.create(
                    suggestion_type=SuggestionGame.SuggestionTypes.BY_GENRE,
                    user=User.objects.get(user=request.user),
                    game_list=" ".join(str(x) for x in game_id_list),
                )

                response = {
                    "game_genre": game_genre_request,
                    "game_list": game_id_list,
                }

                return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"message": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
