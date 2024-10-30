from django.contrib import admin
from .models.User import User
from .models.Genre import Genre
from .models.Game import Game
from .models.Backlog import Backlog
from .models.Wishlist import Wishlist
from .models.SuggestionGame import SuggestionGame


# Custom dashboard models
class UserAdmin(admin.ModelAdmin):
    list_display = ("steam_name", "email", "steam_id", "user")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


class GameAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "release_date",
        "get_genres",  # many to many field
        "platform",
        "steam_app_id",
    )

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = "genres"


class BacklogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "game",
        # "status",
        "rating",
        "comment",
        "playtime",
        "favourite",
    )


class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "order")


# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Backlog, BacklogAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(SuggestionGame)
