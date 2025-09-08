from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.notes import blp as notes_blp

# Initialize Flask app and API with OpenAPI docs
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "Personal Notes API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Group tags for API docs
openapi_tags = [
    {"name": "Healt Check", "description": "Health check route"},
    {"name": "Auth", "description": "User authentication endpoints"},
    {"name": "Notes", "description": "CRUD endpoints for notes"},
]

api = Api(app)
api.spec.tags = openapi_tags  # ensure tags show up in /openapi.json

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(auth_blp)
api.register_blueprint(notes_blp)
