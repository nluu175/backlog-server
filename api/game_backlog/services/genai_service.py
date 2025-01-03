import google.generativeai as genai
from ..environment import GEMINI_API_KEY


class GenAIService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_game_suggestions(self, genre_prompt, game_list):
        """
        Generate game suggestions based on the genre prompt and the game list provided.
            param genre_prompt: The genre of the games to suggest.
            param game_list: A list of games gotten from the backlog.
        """

        prompt_msg = (
            f"From this game list: {game_list}\n"
            f"Suggest up to 5 {genre_prompt} games in this exact Python list format:\n"
            "[(steam_id), ...]"
            "\nOnly return the Python list, no other text. Please select different games each time."
        )

        return self.model.generate_content(prompt_msg)
