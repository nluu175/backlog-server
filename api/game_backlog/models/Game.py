from django.db import models
from django.utils import timezone
from .Genre import Genre


import uuid
import datetime


class Game(models.Model):
    class Meta:
        verbose_name = "game"
        verbose_name_plural = "games"

    class PlatformTypes(models.IntegerChoices):
        PC = 0, "Steam"
        SWITCH = 1, "Switch"

    def __str__(self):
        return f"{self.name} - ({self.id})"

    def was_released_recently(self):
        return self.release_date >= timezone.now() - datetime.timedelta(days=1)

    # This one should be fetch from Steam API and stored in this table
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    release_date = models.DateField(null=True)
    genres = models.ManyToManyField(Genre)
    platform = models.IntegerField(choices=PlatformTypes.choices, null=True)
    steam_app_id = models.IntegerField(unique=True, null=True)
