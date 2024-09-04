from django.db import models

from .User import User

import uuid


class SuggestionGame(models.Model):
    # TODO: Add more types here
    class SuggestionTypes(models.IntegerChoices):
        BY_GENRE = 0, "By Genre"

    class Meta:
        verbose_name = "suggestion game"
        verbose_name_plural = "suggestion games"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    suggestion_type = models.IntegerField(choices=SuggestionTypes.choices, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # can make this into FOREIGN fields
    game_list = models.CharField(
        max_length=1000, null=False
    )  # this is a list of games in string format e.g "game1_id, game2_id, game3_id, ..."

    created_at = models.DateTimeField(auto_now_add=True)  # auto created at creation
    updated_at = models.DateTimeField(auto_now=True)  # auto updated at every save
