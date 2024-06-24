from django.contrib import admin
from .models.User import User
from .models.Genre import Genre
from .models.Game import Game
from .models.Backlog import Backlog

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Backlog)
