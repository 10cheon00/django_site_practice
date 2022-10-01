from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, password=None, **kwargs):
        try:
            user = self.model(name=name, password=password)
            user.set_password(password)
            user.is_active = True

            kwargs.setdefault("is_staff", False)
            kwargs.setdefault("is_superuser", False)
            user.save()

            return user
        except Exception as e:
            print(e)

    def create_superuser(self, name, password=None, **kwargs):
        try:
            superuser = self.create_user(name, password, **kwargs)
            superuser.is_superuser = True
            superuser.is_staff = True
            superuser.is_active = True
            superuser.save()

            return superuser
        except Exception as e:
            print(e)
