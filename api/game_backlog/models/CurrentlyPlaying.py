from django.db import models

from .User import User
from .Game import Game

import uuid


class Wishlist(models.Model):
    def __str__(self):
        return f"{self.user.steam_id} - {self.game.name}"

    # NOTE: Should this be just a field in backlog or a table (more fields in the future?)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    # user and game combination should be unique for each entry
    class Meta:
        verbose_name = "currently_playing"
        verbose_name_plural = "currently_playings"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"], name="unique_currently_playing_user_game"
            )
        ]
