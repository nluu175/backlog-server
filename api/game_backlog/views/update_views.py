from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests

from django.shortcuts import get_object_or_404

from ..models.Game import Game
from ..models.Backlog import Backlog
from ..models.User import User


from ..environment import STEAM_API_KEY


class UpdateView(APIView):
    http_method_names = ["post"]
    
    # TODO: Add serializer

    def post(self, request, steam_id):
        """
        Refresh and update the backlog for user with id steam_id

        :param request: request
        :param steam_id: STEAM ID of the user
        :return: None
        """

        # NOTE: https://www.steamidfinder.com/
        # ---------- Check List
        # 0. Check whether steam_id is CORRECT and EXISTS IN OUR DATABASE (user with that steam_id exists in OUR database)
        # 1. Fetch games list from STEAM API (DONE)
        # 2. Add game(s) to Game table if they do not already exist there (DONE)
        # 3. Add/Update the game in backlog (ASSUME no game is removed)

        # TODO: game logo

        # Source: https://stackoverflow.com/questions/53963328/how-do-i-get-a-hash-for-a-picture-form-a-steam-game

        # ---------------- Pics Format
        # http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg
        # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/hero_capsule.jpg
        # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/capsule_616x353.jpg
        # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/header.jpg
        # https://cdn.cloudflare.steamstatic.com/steam/apps/1569040/capsule_231x87.jpg

        user = get_object_or_404(User, steam_id=steam_id)

        if user:
            data_format = "json"

            try:
                request_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=true&format={data_format}"

                steam_data: Response = requests.get(request_url)
                steam_object = steam_data.json()
                response_field = steam_object.get("response", {})
                games_field = response_field.get("games", {})

                placeholder_description = None
                placeholder_release_date = None
                placeholder_platform = None
                placeholder_genres = ["49941f0a-b60e-4ce0-baf2-378520c00a0a"]

                for game in games_field:
                    game_obj, created = Game.objects.get_or_create(
                        steam_app_id=game["appid"],
                        defaults={
                            "name": game["name"],
                            "description": placeholder_description,
                            "release_date": placeholder_release_date,
                            "platform": placeholder_platform,
                        },
                    )

                    if created:
                        game_obj.genres.set(placeholder_genres)
                        game_obj.save()

                    backlog_entry_status = 0 if game["playtime_forever"] != 0 else 1
                    backlog, backlog_created = Backlog.objects.get_or_create(
                        user=user,
                        game=game_obj,
                        defaults={
                            "status": backlog_entry_status,
                            "rating": 0,
                            "comment": None,
                            "playtime": game["playtime_forever"],
                        },
                    )

                    # backlog_created is False aka. have to update
                    if not backlog_created:
                        backlog.status = 1
                        backlog.rating = 1
                        backlog.playtime = game["playtime_forever"]
                        backlog.save()

                return Response(games_field, status=status.HTTP_200_OK)

            # TODO: Rewrite this
            except requests.exceptions.RequestException as error:
                response_obj = {"message": str(error)}
                return Response(response_obj, status=status.HTTP_400_BAD_REQUEST)
