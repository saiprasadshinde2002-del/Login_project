from .celery_app import celery

@celery.task
def send_welcome_email(user_email):
    print(f"Sending welcome email to {user_email}")
