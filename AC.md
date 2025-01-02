AC:
- POST /api/users: Create User
- GET /api/users: List users
- GET /api/users/{user_id}: Get user by ID
- PATCH /api/users/{user_id}: Update user, require loggedin user and user is updating own profile


- POST /api/rooms: Create new room
- GET /api/rooms: List rooms
- POST /api/rooms/{room_id}/messages: Post new messages
- GET /api/rooms/{room_id}/messages: List room messages
- DELETE /api/rooms/{room_id}/messages/{message_id}: Delete message (own/bonus: admin user deleting) 
- PATCH /api/rooms/{room_id}/messages/{message_id}: for updating a message
