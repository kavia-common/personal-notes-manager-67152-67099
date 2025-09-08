from flask_smorest import Blueprint
from flask.views import MethodView

# Keep name consistent to existing tag but fix description; leaving name as-is to match openapi.json
blp = Blueprint("Healt Check", "health", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    """
    Health check endpoint.
    """
    def get(self):
        return {"message": "Healthy"}
