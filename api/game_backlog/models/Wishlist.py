from django.db import models

from .User import User
from .Game import Game

import uuid


class Wishlist(models.Model):
    def __str__(self):
        return f"{self.user.steam_id} - {self.game.name}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    # NOTE: order is the priority of the game in the wishlist (check STEAM wishlist feature)
    order = models.IntegerField(null=False, default=0)

    # user and game combination should be unique for each entry
    class Meta:
        verbose_name = "wishlist"
        verbose_name_plural = "wishlists"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"], name="unique_wishlist_user_game"
            )
        ]
