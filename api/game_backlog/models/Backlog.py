from django.db import models

from django.contrib.auth.models import User
from .Game import Game

import uuid


class Backlog(models.Model):
    class StatusTypes(models.IntegerChoices):
        NOT_STARTED = 0, "Not Started"
        IN_PROGRESS = 1, "In Progress"
        COMPLETED = 2, "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StatusTypes.choices)
    rating = models.FloatField(null=True, blank=True)  # personal rating
    comment = models.CharField(max_length=1000, null=True)

    # playtime in minutes
    playtime = models.IntegerField(default=0)

    # user and game combination should be unique for each entry
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "game"], name="unique_user_game")
        ]
