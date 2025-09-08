"""
Marshmallow schemas for request validation and OpenAPI docs.
"""
from marshmallow import Schema, fields, validate


class MessageSchema(Schema):
    message = fields.String(required=True, description="Informational message")


class PaginationMetadataSchema(Schema):
    total = fields.Integer()
    total_pages = fields.Integer()
    first_page = fields.Integer()
    last_page = fields.Integer()
    page = fields.Integer()
    previous_page = fields.Integer(allow_none=True)
    next_page = fields.Integer(allow_none=True)


class RegisterRequestSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, validate=validate.Length(min=6), description="User password")


class LoginRequestSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, description="User password")


class AuthResponseSchema(Schema):
    access_token = fields.String(required=True, description="Signed access token")
    token_type = fields.String(required=True, example="bearer")
    expires_in = fields.Integer(required=True, description="Token expiration time in seconds")
    user = fields.Dict(required=True, description="User profile payload")


class UserSchema(Schema):
    id = fields.String(required=True)
    email = fields.Email(required=True)
    created_at = fields.Float(required=True)


class NoteCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200), description="Note title")
    content = fields.String(required=True, description="Note content")


class NoteUpdateSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=200), description="Note title")
    content = fields.String(required=False, description="Note content")


class NoteSchema(Schema):
    id = fields.String(required=True)
    user_id = fields.String(required=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    created_at = fields.Float(required=True)
    updated_at = fields.Float(required=True)
