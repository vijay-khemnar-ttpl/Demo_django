import os
from django.core. mail import send_mail


EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")


def send_registration_mail(user_obj, password):
    send_mail(
        subject="Registration Successful",
        message=f"""Successfully registered on Demo Djnago!
        Username: {user_obj.email}
        Password: {password}
        """,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_obj.email],
        fail_silently=False
    )
