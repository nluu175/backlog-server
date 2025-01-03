from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    game_views,
    genre_views,
    backlog_views,
    update_views,
    auth_views,
    wishlist_views,
    suggestion_views,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Game Backlog API",
        default_version="v1",
        description="Game Backlog API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
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
        "backlogs/user/<uuid:user_id>/",
        backlog_views.BacklogsByUserView.as_view(),
        name="backlogs-filtered-by-user",
    ),
    # Wishlists
    # TODO: Do I really need this? Or can I just use the Backlog model with a wishlist flag?
    path("wishlists/", wishlist_views.WishlistsView.as_view(), name="wishlists"),
    path(
        "wishlists/<uuid:backlog_id>/",
        wishlist_views.WishlistView.as_view(),
        name="wishlist",
    ),
    # Refresh
    path(
        "refresh/<str:user_id>/",
        update_views.UpdateView.as_view(),
        name="backlog-refresh",
    ),
    # Authentication
    path("user/login/", auth_views.LoginView.as_view(), name="user-login"),
    path("user/logout/", auth_views.LogoutView.as_view(), name="user-logout"),
    path("user/signup/", auth_views.SignUpView.as_view(), name="user-signup"),
    # Suggestion
    path(
        "suggestions/", suggestion_views.SuggestionView.as_view(), name="ai-suggestion"
    ),
    # Swagger URLs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
