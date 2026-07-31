from flask_mail import Message
from database.db import mail


def send_reset_email(user):

    token = user.generate_reset_token()

    msg = Message(
        subject="Reset your CALIM password",
        recipients=[user.email]
    )

    msg.body = f"""
Hello {user.full_name},

Click the link below to reset your password.

http://localhost:5173/reset-password/{token}

This link expires in one hour.

If you didn't request a password reset, ignore this email.
"""

    mail.send(msg)