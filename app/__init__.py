from flask import Flask
from flask_cors import CORS
from app.extensions import db
from flask_jwt_extended import JWTManager
from app.routes.product_routes import product_bp
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///beauty_shop.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    JWTManager(app)
    
    app.register_blueprint(product_bp)
    app.register_blueprint(auth_bp)
    
    return app
