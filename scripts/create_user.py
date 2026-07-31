#!/usr/bin/env python3
import argparse
import os
import sys

# Ensure project root is on sys.path when running from the scripts/ folder
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app
from database.db import db, bcrypt
from models.user import User


def create_user(full_name, email, password, phone=None, role="customer"):
    with app.app_context():
        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"User with email {email} already exists (id={existing.id}, role={existing.role}).")
            return

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            full_name=full_name,
            email=email,
            password=hashed,
            phone=phone,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        print(f"Created user {email} (id={user.id}, role={user.role}).")


def main():
    parser = argparse.ArgumentParser(description="Create a user in the CALIM DB without wiping data.")
    parser.add_argument("--full_name", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--phone", default=None)
    parser.add_argument("--role", choices=["admin", "customer"], default="customer")

    args = parser.parse_args()

    create_user(
        full_name=args.full_name,
        email=args.email,
        password=args.password,
        phone=args.phone,
        role=args.role
    )


if __name__ == "__main__":
    main()
