from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, inn, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.username = username
        user.inn = inn
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, **extra_fields):
        extra_fields.setdefault("inn", '0000000000')
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username=username, password=password, email=email, **extra_fields)
