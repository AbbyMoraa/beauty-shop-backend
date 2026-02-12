from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://beautyuser:beautypass@localhost:5432/beautyshop"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "supersecretkey"

    db.init_app(app)

    # ONLY register routes that actually exist
    try:
        from app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
    except ImportError:
        print("Auth routes not yet available")

    return app


