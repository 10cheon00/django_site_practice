import jwt

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.urls import reverse

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import SECRET_KEY
from users.serializers import KakaoRegistrationSerializer
from users.serializers import UserSerializer
from users.utils import create_token_with_user
from users.utils import fetch_kakao_user_data
from users.utils import send_verification_email


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
                user.is_verified = False
                user.save()

            token = create_token_with_user(user)
            current_site = get_current_site(request)
            relative_url = reverse("email-verification")
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
            user.is_verified = True
            user.save()

            return Response(data="?????????????????????.", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            error_msg = "????????? ???????????????."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            error_msg = "???????????? ?????? ???????????????."
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
                raise User.DoesNotExist("???????????? ?????? ??????????????????.")

            token = create_token_with_user(user.first())
            return Response(data=token, status=status.HTTP_200_OK)

        except KeyError as key:
            error_msg = f"{str(key)}????????? ????????? ????????????."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response(data=str(e), status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class KakaoRegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = KakaoRegistrationSerializer

    def post(self, request):
        User = get_user_model()
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            access_token = serializer.data["access_token"]
            kakao_user_data = fetch_kakao_user_data(access_token)
            kakao_user_id = kakao_user_data["id"]

            user = User.objects.filter(
                kakao_id=kakao_user_id, registration_type="kakao"
            )
            if user.exists():
                raise Exception("?????? ?????????????????? ???????????????.")

            username = kakao_user_id
            nickname = serializer.data["nickname"]
            extra_fields = {
                "favorate_race": serializer.data["favorate_race"],
                "registration_type": "kakao",
                "kakao_id": username,
            }
            created_user = User.objects.create_user(
                username=username, nickname=nickname, **extra_fields
            )

            token = create_token_with_user(created_user)
            return Response(data=token, status=status.HTTP_201_CREATED)
        except KeyError as e:
            error_msg = f"{str(e)}????????? ????????? ????????????."
            return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
