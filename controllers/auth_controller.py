from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from database.db import db, bcrypt
from models.user import User
from services.email_service import send_reset_email


# ==========================
# Register User
# ==========================
def register():

    data = request.get_json() or {}

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    phone = data.get("phone", "").strip()

    if not full_name or not email or not password:
        return jsonify({
            "message": "Full name, email and password are required."
        }), 400

    existing = User.query.filter(
        db.func.lower(User.email) == email
    ).first()

    if existing:
        return jsonify({
            "message": "Email already exists."
        }), 409

    role = "customer"

    if User.query.count() == 0:
        role = "admin"

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        phone=phone,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(
        identity=str(new_user.id),
        additional_claims={
            "role": new_user.role
        }
    )

    return jsonify({
        "message": "User registered successfully.",
        "token": access_token,
        "access_token": access_token,
        "role": new_user.role,
        "user": new_user.to_dict()
    }), 201


# ==========================
# Login
# ==========================
def login():

    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required."
        }), 400

    user = User.query.filter(
        db.func.lower(User.email) == email
    ).first()

    if not user:
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "message": "Login successful.",
        "token": access_token,
        "access_token": access_token,
        "role": user.role,
        "user": user.to_dict()
    }), 200


# ==========================
# Logged In User Profile
# ==========================
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({
            "message": "Invalid token identity."
        }), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found."
        }), 404

    return jsonify(user.to_dict()), 200


# ==========================
# Update Profile
# ==========================
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({
            "message": "Invalid token identity."
        }), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found."
        }), 404

    data = request.get_json() or {}

    user.full_name = data.get("full_name", user.full_name)
    user.phone = data.get("phone", user.phone)

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully.",
        "user": user.to_dict()
    }), 200


# ==========================
# Change Password
# ==========================
@jwt_required()
def change_password():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({
            "message": "Invalid token identity."
        }), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found."
        }), 404

    data = request.get_json() or {}

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({
            "message": "Current password and new password are required."
        }), 400

    if not bcrypt.check_password_hash(
        user.password,
        current_password
    ):
        return jsonify({
            "message": "Current password is incorrect."
        }), 401

    user.password = bcrypt.generate_password_hash(
        new_password
    ).decode("utf-8")

    db.session.commit()

    return jsonify({
        "message": "Password changed successfully."
    }), 200


# ==========================
# Forgot Password
# ==========================
def forgot_password():

    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()

    if not email:
        return jsonify({
            "message": "Email is required."
        }), 400

    user = User.query.filter(
        db.func.lower(User.email) == email
    ).first()

    if not user:
        return jsonify({
            "message": "No account found with that email."
        }), 404

    send_reset_email(user)

    return jsonify({
        "message": "Password reset email sent successfully."
    }), 200


# ==========================
# Reset Password
# ==========================
def reset_password(token):

    user = User.verify_reset_token(token)

    if not user:
        return jsonify({
            "message": "Invalid or expired reset token."
        }), 400

    data = request.get_json() or {}

    password = data.get("password")

    if not password:
        return jsonify({
            "message": "Password is required."
        }), 400

    user.password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    db.session.commit()

    return jsonify({
        "message": "Password reset successfully."
    }), 200