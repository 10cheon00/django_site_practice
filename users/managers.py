from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, nickname, password=None, **extra_fields):
        try:
            user = self.model(username=username, nickname=nickname, **extra_fields)
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()

            return user
        except Exception as e:
            print(e)

    def create_superuser(self, username, nickname, password=None, **extra_fields):
        try:
            superuser = self.create_user(
                username=username, nickname=nickname, password=password, **extra_fields
            )
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()

            return superuser
        except Exception as e:
            print(e)
