from django.db import models

from .User import User
from .Game import Game

import uuid


class Backlog(models.Model):
    class StatusTypes(models.IntegerChoices):
        NOT_STARTED = 0, "Not Started"
        IN_PROGRESS = 1, "In Progress"

        # TODO: What make a game "Completed"? Can introduce an option to set the game as "Completed" when the user wants to.
        COMPLETED = 2, "Completed"

    def __str__(self):
        return f"{self.user.steam_id} - {self.game.name} - ({self.id})"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StatusTypes.choices, null=True)
    rating = models.FloatField(null=True, blank=True)  # personal rating
    comment = models.CharField(max_length=1000, null=True)
    # playtime in minutes
    playtime = models.IntegerField(default=0)
    # new
    favourite = models.BooleanField(null=False, default=False)

    # user and game combination should be unique for each entry
    class Meta:
        verbose_name = "backlog"
        verbose_name_plural = "backlogs"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"], name="unique_backlog_user_game"
            )
        ]
