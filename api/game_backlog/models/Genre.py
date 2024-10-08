from django.db import models

import uuid


# NOTE: Source: https://steamdb.info/tags/#genre


class Genre(models.Model):
    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"

    def __str__(self):
        return f"{self.name} - ({self.id})"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # name = display name
    name = models.CharField(max_length=100)
    # code rules:
    # - lower case
    # - spaces are replaced with -
    code = models.CharField(max_length=100, default="", unique=True)
