from flask import request, jsonify

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_jwt
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
            "message":"Full name, email and password are required."
        }),400


    existing_user = User.query.filter(
        db.func.lower(User.email)==email
    ).first()


    if existing_user:
        return jsonify({
            "message":"Email already exists."
        }),409



    # First account becomes admin
    role = "admin" if User.query.count()==0 else "customer"


    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")


    user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        phone=phone,
        role=role
    )


    db.session.add(user)
    db.session.commit()



    token = create_access_token(
        identity=user.id,
        additional_claims={
            "role":user.role
        }
    )


    return jsonify({

        "message":"Registration successful",

        "access_token":token,

        "token":token,

        "user":user.to_dict(),

        "role":user.role

    }),201





# ==========================
# Login
# ==========================

def login():

    data=request.get_json() or {}


    email=data.get("email","").strip().lower()
    password=data.get("password","")



    if not email or not password:

        return jsonify({
            "message":"Email and password required."
        }),400




    user=User.query.filter(
        db.func.lower(User.email)==email
    ).first()



    if not user:

        return jsonify({
            "message":"Invalid email or password."
        }),401




    if not bcrypt.check_password_hash(
        user.password,
        password
    ):

        return jsonify({
            "message":"Invalid email or password."
        }),401




    token=create_access_token(

        identity=user.id,

        additional_claims={
            "role":user.role
        }

    )



    return jsonify({

        "message":"Login successful",

        "access_token":token,

        "token":token,

        "user":user.to_dict(),

        "role":user.role

    }),200





# ==========================
# Profile
# ==========================

def profile():

    user_id=get_jwt_identity()


    user=User.query.get(user_id)



    if not user:

        return jsonify({
            "message":"User not found"
        }),404



    return jsonify({
        "user":user.to_dict()
    }),200





# ==========================
# Update Profile
# ==========================

def update_profile():

    user_id=get_jwt_identity()


    user=User.query.get(user_id)


    data=request.get_json() or {}


    user.full_name=data.get(
        "full_name",
        user.full_name
    )


    user.phone=data.get(
        "phone",
        user.phone
    )


    db.session.commit()


    return jsonify({

        "message":"Profile updated",

        "user":user.to_dict()

    }),200






# ==========================
# Change Password
# ==========================

def change_password():

    user_id=get_jwt_identity()


    user=User.query.get(user_id)


    data=request.get_json() or {}


    current=data.get("current_password")
    new=data.get("new_password")



    if not bcrypt.check_password_hash(
        user.password,
        current
    ):

        return jsonify({
            "message":"Wrong password"
        }),401



    user.password=bcrypt.generate_password_hash(
        new
    ).decode("utf-8")



    db.session.commit()



    return jsonify({
        "message":"Password changed"
    }),200





# ==========================
# Forgot Password
# ==========================

def forgot_password():

    data=request.get_json() or {}

    email=data.get("email","").lower()


    user=User.query.filter(
        db.func.lower(User.email)==email
    ).first()



    if not user:

        return jsonify({
            "message":"Account not found"
        }),404



    send_reset_email(user)


    return jsonify({
        "message":"Reset email sent"
    }),200





# ==========================
# Reset Password
# ==========================

def reset_password(token):

    user=User.verify_reset_token(token)


    if not user:

        return jsonify({
            "message":"Invalid token"
        }),400



    data=request.get_json() or {}


    password=data.get("password")


    user.password=bcrypt.generate_password_hash(
        password
    ).decode("utf-8")



    db.session.commit()



    return jsonify({
        "message":"Password reset successful"
    }),200