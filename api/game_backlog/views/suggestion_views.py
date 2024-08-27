import google.generativeai as genai
import os
import ast

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.Backlog import Backlog


class SuggestionView(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        # TODO: Give the option to cache the result. Can handle this with a parameter REFRESH?
        # Curently only supports suggesting games to play based on the games in the library.

        # TODO: Refactor this genai model to another file so that it can be used in other views
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Fetch my backlog
        game_data = list(
            Backlog.objects.select_related("game").values_list(
                "game__name",
                "game__steam_app_id",
                flat=False,
            )
        )

        game_list = game_data

        game_genre_request = request.query_params.get("game_genre_request", None)
        if game_genre_request is None:
            return Response(
                {"error": "No game_genre_request parameter provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        genre_prompt = game_genre_request

        prompt_msg = (
            "Suggest me a list of games to play."
            + f"The genre is {genre_prompt}. Give the output in python list format like this [(games, steam_id)] and use double quote for string."
            + 'The output example should be like this [("game1", 1234), ("game2", 5678)]. '
            + "Here is the list. "
            + str(game_list)
            + "I want a list of maximum 5 games."
        )

        genai_response = model.generate_content(prompt_msg)

        # # TODO: Add exception for wrong format.
        # # TODO: Refactor this to a function that process string
        genai_response_text = genai_response.text
        try:
            if "python\n" in genai_response_text:
                cleaned_string = (
                    genai_response_text.strip().strip("```python\n").strip("```")
                )

            games_list_processed = ast.literal_eval(cleaned_string)
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
