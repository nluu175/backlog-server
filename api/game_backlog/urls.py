from django.urls import path

from .views import (
    game_views,
    genre_views,
    backlog_views,
    update_views,
    auth_views,
    wishlist_views,
)

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
        "wishlists/",
        wishlist_views.WishlistsView.as_view(),
        name="wishlists",
    ),
    path(
        "wishlists/<uuid:backlog_id>/",
        wishlist_views.WishlistView.as_view(),
        name="wishlist",
    ),
    path(
        "refresh/<str:steam_id>/",
        update_views.UpdateView.as_view(),
        name="backlog-refresh",
    ),
    path(
        "user/login/",
        auth_views.LoginView.as_view(),
        name="user-login",
    ),
    path(
        "user/signup/",
        auth_views.SignUpView.as_view(),
        name="user-signup",
    ),
]
