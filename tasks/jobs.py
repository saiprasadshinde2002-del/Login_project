from .celery_app import celery

import os
import smtplib,ssl
from email.message import EmailMessage

SMTP_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EMAIL_PORT", "587"))
SMTP_USER = os.getenv("EMAIL_USER")           # Use env variable name here, e.g., EMAIL_USER
SMTP_PASS = os.getenv("EMAIL_PASS")           # Use env variable name here, e.g., EMAIL_PASS
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)

@celery.task(bind=True)
def send_welcome_email(self, user_email: str):
    print(f"Sending welcome email to {user_email}")
    subject = "Welcome to Our Platform!"
    body = f"Thank you for signing up {user_email}. We're glad to have you with us. Best regards, The Team"
    _send_gmail(user_email, subject, body)
    return "sent"


def _send_gmail(to_email: str, subject: str, body: str):
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("EMAIL_USER or EMAIL_PASS not set in environment")
    if not EMAIL_FROM:
        raise RuntimeError("EMAIL_FROM not set and EMAIL_USER is empty")

    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5, name="tasks.jobs.send_product_added_email")
def send_product_added_email(self, to_email: str, product_name: str, product_id: int, product_description: str, product_price: float, product_quantity: int, product_tags: list ):
    subject = f"New product added: {product_name}"
    body = f"(ID: {product_id}), Product - {product_name}, product_description:{product_description}, product_price - {product_price}, product_quantity{product_quantity}, product_tags{product_tags}, was just added."
    _send_gmail(to_email, subject, body)    
    return "sent"