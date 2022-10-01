from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ("email", "Email"),
        ("kakao", "Kakao"),
    ]
    RACE_LIST = [
        ("terran", "Terran"),
        ("zerg", "Zerg"),
        ("protoss", "Protoss"),
        ("random", "Random"),
    ]

    registration_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0]
    )
    user_id = models.CharField(max_length=100, unique=True)
    clan_id = models.CharField(max_length=100, unique=True)
    favorate_race = models.CharField(max_length=10, choices=RACE_LIST)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = [
        "clan_id",
    ]

    kakao_id = models.BigIntegerField(default=0, null=True)

    objects = UserManager()
