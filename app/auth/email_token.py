from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv
from fastapi import  BackgroundTasks
from fastapi_mail import  MessageSchema
from app.config import  fm
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SALT = "email-verification"

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_verification_token(email: str):
    return serializer.dumps(email, salt=SALT)

def confirm_verification_token(token: str, expiration=3600):
    return serializer.loads(token, salt=SALT, max_age=expiration)

async def send_verification_email(background_tasks: BackgroundTasks, email: str):
    token = generate_verification_token(email)
    verify_link = f"{os.getenv("FRONTEND_URL")}/verify-email?token={token}"

    message = MessageSchema(
        subject="Verify your Email",
        recipients=[email],
        body=f"<p>Click <a href='{verify_link}'>here</a> to verify your Face Trust account.</p>",
        subtype="html"
    )

    background_tasks.add_task(fm.send_message, message)
    return {"message": "Verification email sent"}