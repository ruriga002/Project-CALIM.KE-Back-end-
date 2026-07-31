import os
from dotenv import load_dotenv

load_dotenv()


def get_database_uri():
    database_url = os.getenv("DATABASE_URL", "").strip()

    if database_url and database_url != "postgresql://postgres:YOUR_PASSWORD@localhost:5432/calim_db":
        return database_url

    return "sqlite:///calim_dev.db"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "calim_secret_key")

    SQLALCHEMY_DATABASE_URI = get_database_uri()

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "calim_jwt_secret")

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")

    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))

    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"

    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your_email@gmail.com")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your_app_password")