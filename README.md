# Backlog Server

## Introduction

- Welcome to the Backlog API documentation. This API was implemented to serve the Game Backlog App - A web-based application to help manage your game backlog in many gaming platforms.

## TODO:

Here is the content in a markdown table format:

| Task                                                                                                                                                         | Status                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| Add transactions [Official Doc](https://docs.djangoproject.com/en/5.1/topics/db/transactions/) <br> - `with transaction.atomic():`                           | DONE                   |
| Integrate Gemini <br> - Suggest game to play based on genre (in library) <br> - Suggest game to play (not in library)? <br> - Suggest a random game to play? | <br> DONE <br> NOT-YET |
| User can add friend                                                                                                                                          | -                      |
| Add games release tracker (web scraping)                                                                                                                     | BIG                    |
| Add price(float) in Game                                                                                                                                     | UNDER CONSIDERATION    |
| Support other platforms (eshop/Nintendo)                                                                                                                     | -                      |
| Authenticate/Authorize using token                                                                                                                           | DONE                   |
| Add table GameSuggestion to cache game request result                                                                                                        | DONE                   |
| Move all Error and Exception to errors.py                                                                                                                    | DONE                   |
| Add "How long to beat" a game estimation                                                                                                                     | -                      |
| Add a table to keep track of "Game I wanna play currently"                                                                                                   | -                      |
| Add `first` and `last` fields for pagination                                                                                                                 | -                      |

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

- UpdateGame

  - make api /user_id/ instead of /steam_id/ [DONE]
  - this will get the steam_id of the given user_id [DONE]
  - improve logic for update game endpoint
