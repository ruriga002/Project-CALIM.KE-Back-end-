from datetime import datetime
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

from database.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="customer",
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
   

    orders = db.relationship(
        "Order",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    cart_items = db.relationship(
        "Cart",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    # Password Reset

    def generate_reset_token(self):
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        return serializer.dumps(
            self.email,
            salt="password-reset"
        )

    @staticmethod
    def verify_reset_token(token, expires_sec=3600):

        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        try:
            email = serializer.loads(
                token,
                salt="password-reset",
                max_age=expires_sec
            )

        except Exception:
            return None

        return User.query.filter_by(
            email=email
        ).first()
    
    # Serialize User

    def to_dict(self):

        is_admin = self.role == "admin"

        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "is_admin": is_admin,
            "isAdmin": is_admin,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    # String Representation
    

    def __repr__(self):

        return f"<User {self.email}>"