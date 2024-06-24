from django.urls import path

from .views import game_views, genre_views, backlog_views, update_views

urlpatterns = [
    # Games
    path("games/", game_views.GamesView.as_view(), name="games"),
    path("games/<uuid:game_id>/", game_views.GameView.as_view(), name="game"),
    # Genres
    path("genres/", genre_views.GenresView.as_view(), name="genres"),
    path("genres/<uuid:genre_id>/", genre_views.GenreView.as_view(), name="genre"),
    # Backlogs
    path("backlogs/", backlog_views.BacklogsView.as_view(), name="backlogs"),
    path(
        "backlogs/<uuid:backlog_id>/",
        backlog_views.BacklogView.as_view(),
        name="backlog",
    ),
    path(
        "refresh/<str:steam_id>/",
        update_views.UpdateView.as_view(),
        name="backlog-refresh",
    ),
]
