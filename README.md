# Async SQLAlchemy in FastAPI

To interact with the database asynchronously, this project uses aiosqlite.

## Available routes

- `POST /api/users`: Create user
- `GET /api/users`: List users
- `GET /api/users/{user_id}`: Get user by ID
- `PATCH /api/users/{user_id}`: Update user, require user to be logged in and
  ensure user is updating own account
- `POST /api/rooms`: Create new room
- `GET /api/rooms`: List rooms
- `POST /api/rooms/{room_id}/messages`: Post new message
- `GET /api/rooms/{room_id}/messages`: List room messages
- `DELETE /api/rooms/{room_id}/messages/{message_id}`: Delete message
- `PATCH /api/rooms/{room_id}/messages/{message_id}`: Update a message

## Running the server

Create and activate virtual environment

```
pyenv virtualenv 3.11.5 myenv
pyenv activate myenv
```

Install the dependencies

```
pip install -r requirements.txt
```

Start the app

```
uvicorn src.main:app --reload
```

## Authentication / Authorization

You can either login and get your `Bearer` token, or put in some variation of
`pleeeez` (with as many `e`s as you like) as the token, and do the same in the
`User-Agent` header field, to get admin level privileges.

Keep in mind that you do need a valid token for some routes, such as creating a
message, because your user ID is encoded in the tokens generated by the server.
Without a valid token, it won't know who sent the message.
