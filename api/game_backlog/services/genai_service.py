import google.generativeai as genai
from ..environment import GEMINI_API_KEY


class GenAIService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_game_suggestions(self, genre_prompt, game_list):
        prompt_msg = (
            "Suggest me a list of games to play."
            + f"The genre is {genre_prompt}. Give the output in python list format like this [(games, steam_id)] and use double quote for string."
            + 'The output example should be like this [("game1", game1_id), ("game2", game2_id)]. '
            + "Here is the list. "
            + str(game_list)
            + "List must have maximum 5 games."
        )

        return self.model.generate_content(prompt_msg)
