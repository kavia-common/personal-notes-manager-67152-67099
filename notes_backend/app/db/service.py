"""
Database service abstraction layer for the notes_backend.

This module defines interfaces and a simple in-memory fallback implementation
to abstract database operations so the backend can be wired to the 'notes_database'
dependency in the future without changing route logic.

Do NOT hardcode configuration values; use environment variables provided by the
deployment orchestrator in the .env file when integrating a real database.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Dict
import os
import uuid
import time


@dataclass
class UserRecord:
    id: str
    email: str
    password_hash: str
    created_at: float


@dataclass
class NoteRecord:
    id: str
    user_id: str
    title: str
    content: str
    created_at: float
    updated_at: float


class AbstractDBService:
    """Abstract interface for DB operations used by the backend."""

    # PUBLIC_INTERFACE
    def create_user(self, email: str, password_hash: str) -> UserRecord:
        """Create a new user record."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def get_user_by_email(self, email: str) -> Optional[UserRecord]:
        """Retrieve a user by email if exists."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def get_user_by_id(self, user_id: str) -> Optional[UserRecord]:
        """Retrieve a user by id if exists."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def create_note(self, user_id: str, title: str, content: str) -> NoteRecord:
        """Create a note for a user."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def list_notes(self, user_id: str) -> List[NoteRecord]:
        """List all notes for a user."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def get_note(self, user_id: str, note_id: str) -> Optional[NoteRecord]:
        """Get a specific note for a user."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def update_note(self, user_id: str, note_id: str, title: Optional[str], content: Optional[str]) -> Optional[NoteRecord]:
        """Update a note's title/content for a user."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def delete_note(self, user_id: str, note_id: str) -> bool:
        """Delete a note and return True if deleted."""
        raise NotImplementedError


class InMemoryDBService(AbstractDBService):
    """
    Fallback in-memory implementation for development and CI.
    Replace with real implementation using the 'notes_database' dependency.
    """

    def __init__(self) -> None:
        # Simple structures to simulate persistence
        self._users_by_id: Dict[str, UserRecord] = {}
        self._users_by_email: Dict[str, str] = {}  # email -> user_id
        self._notes_by_user: Dict[str, Dict[str, NoteRecord]] = {}

    def create_user(self, email: str, password_hash: str) -> UserRecord:
        if email in self._users_by_email:
            raise ValueError("User already exists")
        user_id = str(uuid.uuid4())
        now = time.time()
        rec = UserRecord(id=user_id, email=email, password_hash=password_hash, created_at=now)
        self._users_by_id[user_id] = rec
        self._users_by_email[email] = user_id
        self._notes_by_user[user_id] = {}
        return rec

    def get_user_by_email(self, email: str) -> Optional[UserRecord]:
        uid = self._users_by_email.get(email)
        return self._users_by_id.get(uid) if uid else None

    def get_user_by_id(self, user_id: str) -> Optional[UserRecord]:
        return self._users_by_id.get(user_id)

    def create_note(self, user_id: str, title: str, content: str) -> NoteRecord:
        if user_id not in self._notes_by_user:
            self._notes_by_user[user_id] = {}
        note_id = str(uuid.uuid4())
        now = time.time()
        rec = NoteRecord(id=note_id, user_id=user_id, title=title, content=content, created_at=now, updated_at=now)
        self._notes_by_user[user_id][note_id] = rec
        return rec

    def list_notes(self, user_id: str) -> List[NoteRecord]:
        return list(self._notes_by_user.get(user_id, {}).values())

    def get_note(self, user_id: str, note_id: str) -> Optional[NoteRecord]:
        return self._notes_by_user.get(user_id, {}).get(note_id)

    def update_note(self, user_id: str, note_id: str, title: Optional[str], content: Optional[str]) -> Optional[NoteRecord]:
        rec = self._notes_by_user.get(user_id, {}).get(note_id)
        if not rec:
            return None
        if title is not None:
            rec.title = title
        if content is not None:
            rec.content = content
        rec.updated_at = time.time()
        return rec

    def delete_note(self, user_id: str, note_id: str) -> bool:
        user_notes = self._notes_by_user.get(user_id)
        if not user_notes or note_id not in user_notes:
            return False
        del user_notes[note_id]
        return True


# PUBLIC_INTERFACE
def get_db_service() -> AbstractDBService:
    """
    Factory to get the DB service implementation.

    Uses environment variables to decide the implementation. If a real database
    is configured (e.g., NOTES_DB_URL or related vars), a real client should be
    initialized here. Otherwise, fallback to InMemoryDBService.

    Env vars that may be used when integrating the real DB:
    - NOTES_DB_URL
    - NOTES_DB_USER
    - NOTES_DB_PASSWORD
    - NOTES_DB_NAME
    - NOTES_DB_PORT
    """
    # Placeholder selection logic. Currently always returns in-memory.
    # Future integration point: replace with real implementation and keep signature stable.
    _ = os.environ.get("NOTES_DB_URL")
    return InMemoryDBService()
