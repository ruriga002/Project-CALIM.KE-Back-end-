from flask import Blueprint

from flask_jwt_extended import jwt_required

from controllers.auth_controller import (
    register,
    login,
    profile,
    update_profile,
    change_password,
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
@jwt_required()
def get_profile():
    return profile()



@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def edit_profile():
    return update_profile()



@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def update_password():
    return change_password()