from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import register_user, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return register_user(data)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data)

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()   # This will be a string of the user id
    claims = get_jwt()             # Get additional_claims (role)
    role = claims.get("role")

    return jsonify({
        "message": "This is a protected route",
        "user_id": user_id,
        "role": role
    }), 200



