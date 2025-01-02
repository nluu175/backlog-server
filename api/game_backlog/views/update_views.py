from typing import Any, Dict, Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpRequest

import requests
import random

from ..models.Game import Game
from ..models.Backlog import Backlog
from ..models.User import User
from ..models.Genre import Genre

from ..environment import STEAM_API_KEY


class UpdateView(APIView):
    """View for updating user's Steam game backlog."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    # TODO:
    #     To avoid checking games ...
    #         Only check games with date added later than last refresh?

    # NOTE: https://www.steamidfinder.com/
    # ---------- Check List
    # 0. Check whether steam_id is CORRECT and EXISTS IN OUR DATABASE (user with that steam_id exists in OUR database)
    # 1. Fetch games list from STEAM API (DONE)
    # 2. Add game(s) to Game table if they do not already exist there (DONE)
    # 3. Add/Update the game in backlog (ASSUME no game is removed)

    # Source: https://stackoverflow.com/questions/53963328/how-do-i-get-a-hash-for-a-picture-form-a-steam-game

    # ---------------- Pics Format
    # http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg
    # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/hero_capsule.jpg
    # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/capsule_616x353.jpg
    # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/header.jpg
    # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/capsule_231x87.jpg

    # url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"

    STEAM_API_ENDPOINT = (
        "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    )

    # NOTE: THIS IS HARDCODED
    # NOTE: Currently using random_genres test without hardcoding
    DEFAULT_GENRES = ["ff14eb09-1297-4100-8435-7198434663a4"]

    def _random_genres(self):
        """Get random genres from the database."""
        # Get all genre IDs
        genre_ids = list(Genre.objects.values_list("id", flat=True))

        # Randomly select 1-3 genres
        num_genres = random.randint(1, 3)

        # If we have fewer genres than num_genres, use all available genres
        num_genres = min(num_genres, len(genre_ids))

        # Randomly select genre IDs
        selected_genres = random.sample(genre_ids, num_genres)

        return selected_genres

    def _fetch_steam_games(self, steam_id: str) -> Dict[str, Any]:
        """Fetch games from Steam API for given steam_id."""
        params = {
            "key": STEAM_API_KEY,
            "steamid": steam_id,
            "include_appinfo": "true",
            "format": "json",
        }

        response = requests.get(self.STEAM_API_ENDPOINT, params=params)
        response.raise_for_status()

        data = response.json()
        return data.get("response", {}).get("games", {})

    def _create_or_update_game(self, game_data: Dict[str, Any]) -> Game:
        """Create or update a game record."""
        game_obj, created = Game.objects.get_or_create(
            steam_app_id=game_data["appid"],
            defaults={
                "name": game_data["name"],
                "description": None,
                "release_date": None,
                "platform": None,
            },
        )

        if created:
            # game_obj.genres.set(self.DEFAULT_GENRES)
            game_obj.genres.set(self.random_genres)
            game_obj.save()

        return game_obj

    def _update_backlog(self, user: User, game_obj: Game, playtime: int) -> None:
        """Create or update a backlog entry."""

        backlog, created = Backlog.objects.get_or_create(
            user=user,
            game=game_obj,
            defaults={
                "rating": None,
                "comment": None,
                "playtime": playtime,
            },
        )

        if not created:
            backlog.playtime = playtime
            backlog.save()

    @transaction.atomic
    def post(self, request: HttpRequest, steam_id: str) -> Response:
        """
        Refresh and update the backlog for user with id steam_id.

        Args:
            request: HTTP request object
            steam_id: Steam ID of the user

        Returns:
            Response with updated games data or error message
        """
        user = get_object_or_404(User, steam_id=steam_id)

        try:
            games_data = self._fetch_steam_games(steam_id)

            for game_data in games_data:
                game_obj = self._create_or_update_game(game_data)
                self._update_backlog(user, game_obj, game_data["playtime_forever"])

            return Response(games_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as error:
            return Response(
                {"message": f"Steam API error: {str(error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
