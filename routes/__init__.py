# routes/__init__.py - Blueprint Registration
from .auth import auth_bp
from .admin import admin_bp

def register_blueprints(app):
    """Register all blueprints """
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
