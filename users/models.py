from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ("email", "Email"),
        ("kakao", "Kakao"),
    ]

    registration_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0]
    )
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=100, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "name"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
    ]

    objects = UserManager()
