# Backlog Server

## Introduction

- Welcome to the Backlog API documentation. This API was implemented to serve the Game Backlog App - A web-based application to help manage your game backlog in many gaming platforms.

## Instructions

- Run the import data command to import all the game genres (can be found in `commands/`)
- Run `source venv`
- Add `Authorization` header to each request. The template should be `Token {token}`. Token can be gotten from making a login request.
- Run `python manage.py import_genres_data` to import all the predefined data

TODO:

- GameSuggestion

  - make api /user_id/ [DONE] => This currently get user info from request token
  - add other params for game suggestion
  - consider using this schema
    > - /api/suggestions/{type}
    >   -- type: ["genre", "mood", "length"]
    >   -- length can be: ["short", "medium", "long"]
  - filter game suggestion by `completed = True`
  - how long to beat?

  - NOTE: We can tune the model to work for ... only

- UpdateGame

  - make api /user_id/ instead of /steam_id/ [DONE]
  - this will get the steam_id of the given user_id [DONE]
  - improve logic for update game endpoint

- UpdateGame

  - remove temporary random generated genres

- Parse Game Description from Steam API

- Can add average score from steam to the game rating field (Game.steam_rating)

- Add a game release tracker
