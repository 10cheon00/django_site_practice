import requests

from django.core.mail import EmailMessage

from rest_framework_simplejwt.tokens import RefreshToken

from users.exceptions import KakaoException


def create_token_with_user(user):
    refresh = RefreshToken.for_user(user)
    token = {"access": str(refresh.access_token), "refresh": str(refresh)}
    return token


def send_verification_email(data):
    email = EmailMessage(
        body=data["email_body"], subject=data["email_subject"], to=(data["to_email"],)
    )
    email.send()


def fetch_kakao_user_data(access_token):
    try:
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise KakaoException("잘못된 엑세스 토큰입니다.")

        user_data = response.json()
        return user_data
    except Exception as exception:
        raise exception
