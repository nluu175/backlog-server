from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import uuid
import datetime


# TODO: READ MORE INTO DATABASE DESIGN
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    steam_id = models.CharField(max_length=100, null=True)

    # One to One object with django default user
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Genre(models.Model):
    def __str__(self):
        return self.name + f" - ({self.id})"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # name = display name
    name = models.CharField(max_length=100)
    # code rules:
    # - lower case
    # - spaces are replaced with -
    code = models.CharField(max_length=100, default="", unique=True)


class Game(models.Model):
    def __str__(self):
        return self.name + f" - ({self.id})"

    def was_released_recently(self):
        return self.release_date >= timezone.now() - datetime.timedelta(days=1)

    # This one should be fetch from Steam API and stored in this table
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    release_date = models.DateField(null=True)
    genres = models.ManyToManyField(Genre)
    platform = models.CharField(max_length=100, null=True)
    steam_app_id = models.IntegerField(unique=True)


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
