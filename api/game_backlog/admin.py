from django.contrib import admin
from .models.models import User, Genre, Game, Backlog

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Backlog)
