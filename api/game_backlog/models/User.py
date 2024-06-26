from django.db import models
from django.contrib.auth.models import User

import uuid


class User(models.Model):
    def __str__(self):
        return f"[{self.username}] - [{self.steam_id}] - ({self.id})"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    steam_id = models.CharField(max_length=100, null=True)

    # One to One object with django default user
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
