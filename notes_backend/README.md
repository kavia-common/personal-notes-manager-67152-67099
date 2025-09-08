# Notes Backend

Flask backend providing:
- Auth: POST /auth/register, POST /auth/login
- Notes CRUD: GET/POST /notes, GET/PATCH/DELETE /notes/{note_id}
- Health: GET /

Docs available at /docs

Auth
- Send Authorization: Bearer <token> header for all /notes endpoints.
- SECRET_KEY environment variable should be set in production to sign tokens.

Database
- DB operations are abstracted via app/db/service.py.
- Current implementation uses in-memory storage for development/CI.
- To integrate with a real 'notes_database' service, implement AbstractDBService and update get_db_service() to return the concrete implementation using environment vars (e.g., NOTES_DB_URL, NOTES_DB_USER, NOTES_DB_PASSWORD, NOTES_DB_NAME, NOTES_DB_PORT).

Environment variables (example)
- SECRET_KEY=please-change
- NOTES_DB_URL=...
- NOTES_DB_USER=...
- NOTES_DB_PASSWORD=...
- NOTES_DB_NAME=...
- NOTES_DB_PORT=...

Run
- python run.py
