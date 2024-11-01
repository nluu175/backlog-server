# Backlog Server

## Introduction

- Welcome to the Backlog API documentation. This API was implemented to serve the Game Backlog App - A web-based application to help manage your game backlog in many gaming platforms.

## TODO:

- Add transactions [Official Doc](https://docs.djangoproject.com/en/5.1/topics/db/transactions/)
  > - `with transaction.atomic():` [DONE]
- Integrate Gemini

  > - Suggest game to play based on genre (in library) [DONE]
  > - Suggest game to play (not in library)? [NOT-YET]
  > - Suggest a random game to play?

- User can add friend

- Add games release tracker (web scraping) [BIG]

- Add price(float) in Game [UNDER CONSIDERATION]

- Support other platforms (eshop/Nintendo)

- Authenticate/Authorize using token [DONE]

- Add table GameSuggestion to cache game request result. [DONE]

- Move all Error and Exception to errors.py [DONE]

- Add "How long to beat" a game estimation.

- Add a table to keep track of "Game I wanna play currently"

## Instructions

- Run the import data command to import all the game genres (can be found in `commands/`)
- Run `source venv`
- Add `Authorization` header to each request. The template should be `Token {token}`
