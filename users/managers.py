from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, user_id, clan_id, password=None, **kwargs):
        try:
            user = self.model(user_id=user_id, password=password, clan_id=clan_id)
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()

            return user
        except Exception as e:
            print(e)

    def create_superuser(self, user_id, clan_id, password=None, **kwargs):
        try:
            superuser = self.create_user(
                user_id=user_id, clan_id=clan_id, password=password, **kwargs
            )
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()

            return superuser
        except Exception as e:
            print(e)
