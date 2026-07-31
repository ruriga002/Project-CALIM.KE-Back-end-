from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from middleware.auth import jwt_required_custom

from controllers.auth_contoller import (
    register,
    login,
    profile,
    forgot_password,
    reset_password
)

auth_bp = Blueprint(
    "auth",
    __name__
)

# ==========================
# Public Routes
# ==========================

@auth_bp.route("/register", methods=["POST"])
def register_user():
    return register()


@auth_bp.route("/login", methods=["POST"])
def login_user():
    return login()


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot():
    return forgot_password()


@auth_bp.route("/reset-password/<string:token>", methods=["POST"])
def reset(token):
    return reset_password(token)


# ==========================
# Protected Routes
# ==========================

@auth_bp.route("/profile", methods=["GET"])
@jwt_required_custom
def get_profile():

    user_id = get_jwt_identity()

    return profile(user_id)