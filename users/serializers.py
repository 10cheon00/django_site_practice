from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "nickname", "email", "favorate_race", "password"]


class KakaoRegistrationSerializer(ModelSerializer):
    access_token = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ["access_token", "nickname", "favorate_race"]
