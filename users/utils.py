from django.core.mail import EmailMessage

from rest_framework_simplejwt.tokens import RefreshToken


def create_token_with_user(user):
    refresh = RefreshToken.for_user(user)
    token = {"access": str(refresh.access_token), "refresh": str(refresh)}
    return token


def send_verification_email(data):
    email = EmailMessage(
        body=data["email_body"], subject=data["email_subject"], to=(data["to_email"],)
    )
    email.send()
