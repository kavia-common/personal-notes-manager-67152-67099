from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.db.service import get_db_service
from app.auth.utils import hash_password, verify_password, create_access_token
from app.schemas import RegisterRequestSchema, LoginRequestSchema, AuthResponseSchema, UserSchema

blp = Blueprint(
    "Auth",
    "auth",
    url_prefix="/auth",
    description="User authentication endpoints (register, login)"
)


@blp.route("/register")
class Register(MethodView):
    """
    Register a new user.

    Request body:
      - email: string (email)
      - password: string (min 6 chars)

    Response:
      - JSON with access token and user data.
    """
    @blp.arguments(RegisterRequestSchema, location="json")
    @blp.response(201, AuthResponseSchema)
    def post(self, payload):
        """
        summary: Register a new user
        description: Create a user and returns an access token.
        """
        db = get_db_service()
        if db.get_user_by_email(payload["email"]):
            abort(409, message="User already exists")
        user = db.create_user(email=payload["email"], password_hash=hash_password(payload["password"]))
        token, ttl = create_access_token(user.id, user.email)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": ttl,
            "user": UserSchema().dump(user),
        }


@blp.route("/login")
class Login(MethodView):
    """
    Login an existing user.

    Request body:
      - email
      - password

    Response:
      - JSON with access token and user data.
    """
    @blp.arguments(LoginRequestSchema, location="json")
    @blp.response(200, AuthResponseSchema)
    def post(self, payload):
        """
        summary: Login
        description: Verify credentials and return an access token.
        """
        db = get_db_service()
        user = db.get_user_by_email(payload["email"])
        if not user or not verify_password(payload["password"], user.password_hash):
            abort(401, message="Invalid credentials")
        token, ttl = create_access_token(user.id, user.email)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": ttl,
            "user": UserSchema().dump(user),
        }
