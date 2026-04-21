import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from database import SessionLocal
import models
from celery import Celery
from pydantic_settings import BaseSettings

class Worker_Settings(BaseSettings):
    SENDER_EMAIL:str
    SENDER_PASSWORD:str

    class Config:
        env_file = ".env"
        extra = "ignore"

worker_settings = Worker_Settings()

celery_app = Celery("tasks", broker = os.environ.get("CELERY_BROKER_URL"))

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

@celery_app.task
def send_registration_email(user_email):
    try:
        message = MIMEMultipart()
        message["FROM"] = worker_settings.SENDER_EMAIL
        message["TO"] = user_email
        message["SUBJECT"] = "Signup: SpendWisely"
        body = "You recently signed up at Spendwisely"
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(worker_settings.SENDER_EMAIL, worker_settings.SENDER_PASSWORD)
            server.send_message(message)
        return f"email sent to {user_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}" 

