from flask import request, jsonify
from flask_jwt_extended import create_access_token

from database.db import db, bcrypt
from models.user import User
from services.email_service import send_reset_email


# ==========================
# Register User
# ==========================
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    if not full_name or not email or not password:
        return jsonify({
            "message": "Full name, email and password are required."
        }), 400

    existing = User.query.filter_by(email=email).first()

    if existing:
        return jsonify({
            "message": "Email already exists."
        }), 409

    # First registered user becomes admin
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

    return jsonify({
        "message": "User registered successfully.",
        "user": new_user.to_dict()
    }), 201


# ==========================
# Login
# ==========================
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required."
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "message": "Login successful.",
        "token": access_token,
        "user": user.to_dict()
    }), 200


# ==========================
# User Profile
# ==========================
def profile(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found."
        }), 404

    return jsonify(user.to_dict()), 200


# ==========================
# Forgot Password
# ==========================
def forgot_password():

    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({
            "message": "Email is required."
        }), 400

    user = User.query.filter_by(email=email).first()

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

    data = request.get_json()

    password = data.get("password")

    if not password:
        return jsonify({
            "message": "Password is required."
        }), 400

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    user.password = hashed_password

    db.session.commit()

    return jsonify({
        "message": "Password reset successfully."
    }), 200