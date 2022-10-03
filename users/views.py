import jwt

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.urls import reverse

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import SECRET_KEY
from users.serializers import UserSerializer
from users.utils import create_token_with_user
from users.utils import fetch_kakao_user_data
from users.utils import send_verification_email


class PasswordLogInAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        User = get_user_model()
        try:
            user = authenticate(
                username=request.data["username"], password=request.data["password"]
            )
            if user is None:
                raise User.DoesNotExist("아이디 또는 비밀번호가 잘못되었습니다.")
            token = create_token_with_user(user)
            return Response(data=token, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class EmailRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer = UserSerializer

    def post(self, request):
        User = get_user_model()
        with transaction.atomic():
            serializer = self.serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                form_data = serializer.data

                user = User.objects.create_user(
                    username=form_data.pop("username"),
                    nickname=form_data.pop("nickname"),
                    password=form_data.pop("password"),
                    **form_data,
                )
                user.is_active = False
                user.save()

            token = create_token_with_user(user)
            current_site = get_current_site(request)
            relative_url = reverse("verify-email")
            absolute_url = (
                f"http://{current_site}{relative_url}?token={token.get('access')}"
            )
            email_body = f"Hello {user.nickname}, Use link below to verify your account.\n{absolute_url}"
            data = {
                "email_body": email_body,
                "email_subject": "Verify your email",
                "to_email": user.email,
            }

            send_verification_email(data)

            return Response(data=token, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        User = get_user_model()
        token = request.query_params.get("token")
        try:
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            user.is_active = True
            user.save()

            return Response(data="인증되었습니다.", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            error_msg = "만료된 토큰입니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            error_msg = "유효하지 않은 토큰입니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class KakaoLogInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        User = get_user_model()
        try:
            access_token = request.data["access_token"]
            kakao_user_data = fetch_kakao_user_data(access_token)
            kakao_user_id = kakao_user_data["id"]

            user = User.objects.filter(
                kakao_id=kakao_user_id, registration_type="kakao"
            )
            if not user.exists():
                raise User.DoesNotExist("가입되지 않은 사용자입니다.")

            token = create_token_with_user(user.first())
            return Response(data=token, status=status.HTTP_200_OK)

        except KeyError as key:
            error_msg = f"{str(key)}필드에 오류가 있습니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class KakaoRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        User = get_user_model()
        try:
            access_token = request.data["access_token"]
            kakao_user_data = fetch_kakao_user_data(access_token)
            kakao_user_id = kakao_user_data["id"]

            user = User.objects.filter(
                kakao_id=kakao_user_id, registration_type="kakao"
            )
            if user.exists():
                raise Exception("이미 가입되어있는 유저입니다.")

            username = kakao_user_id
            nickname = request.data["nickname"]
            extra_fields = {
                "favorate_race": request.data["favorate_race"],
                "registration_type": "kakao",
                "kakao_id": username,
            }
            created_user = User.objects.create_user(
                username=username, nickname=nickname, **extra_fields
            )

            token = create_token_with_user(created_user)
            return Response(data=token, status=status.HTTP_201_CREATED)
        except KeyError as e:
            error_msg = f"{str(e)}필드에 오류가 있습니다."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
