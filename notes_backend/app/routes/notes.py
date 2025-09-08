from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db.service import get_db_service
from app.auth.utils import verify_access_token
from app.schemas import NoteSchema, NoteCreateSchema, NoteUpdateSchema

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD endpoints for personal notes"
)


def _get_current_user_id() -> str:
    """
    Extract user id from Authorization: Bearer <token> header.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.lower().startswith("bearer "):
        abort(401, message="Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1].strip()
    payload = verify_access_token(token)
    if not payload:
        abort(401, message="Invalid or expired token")
    return payload["sub"]


@blp.route("")
class NotesListCreate(MethodView):
    """
    List notes and create notes for the authenticated user.
    """

    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """
        summary: List notes
        description: Returns the list of notes for the authenticated user.
        """
        user_id = _get_current_user_id()
        db = get_db_service()
        notes = db.list_notes(user_id)
        return [NoteSchema().dump(n) for n in notes]

    @blp.arguments(NoteCreateSchema, location="json")
    @blp.response(201, NoteSchema)
    def post(self, payload):
        """
        summary: Create note
        description: Create a new note for the authenticated user.
        """
        user_id = _get_current_user_id()
        db = get_db_service()
        created = db.create_note(user_id=user_id, title=payload["title"], content=payload["content"])
        return NoteSchema().dump(created)


@blp.route("/<string:note_id>")
class NoteDetail(MethodView):
    """
    Retrieve, update, and delete a specific note for the authenticated user.
    """

    @blp.response(200, NoteSchema)
    def get(self, note_id: str):
        """
        summary: Get note
        description: Retrieve a specific note by id.
        """
        user_id = _get_current_user_id()
        db = get_db_service()
        rec = db.get_note(user_id, note_id)
        if not rec:
            abort(404, message="Note not found")
        return NoteSchema().dump(rec)

    @blp.arguments(NoteUpdateSchema, location="json")
    @blp.response(200, NoteSchema)
    def patch(self, payload, note_id: str):
        """
        summary: Update note
        description: Update title and/or content of a note.
        """
        user_id = _get_current_user_id()
        db = get_db_service()
        rec = db.update_note(user_id, note_id, title=payload.get("title"), content=payload.get("content"))
        if not rec:
            abort(404, message="Note not found")
        return NoteSchema().dump(rec)

    @blp.response(204)
    def delete(self, note_id: str):
        """
        summary: Delete note
        description: Delete a note by id.
        """
        user_id = _get_current_user_id()
        db = get_db_service()
        ok = db.delete_note(user_id, note_id)
        if not ok:
            abort(404, message="Note not found")
        return ""
