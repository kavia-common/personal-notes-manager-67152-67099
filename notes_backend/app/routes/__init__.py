"""
Routes package initializer for notes_backend.

Exports available blueprints for convenient imports.
"""

# PUBLIC_INTERFACE
def available_blueprints():
    """Return the list of available blueprints in this package."""
    from .health import blp as health_blp
    from .auth import blp as auth_blp
    from .notes import blp as notes_blp
    return [health_blp, auth_blp, notes_blp]
