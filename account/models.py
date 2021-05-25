from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    inn = models.CharField(
        _("ИНН"),
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex='^\d{10}$', message='Should be 10 digits number')],
    )
    account = models.DecimalField(_("Счет"), max_digits=11, decimal_places=2, default=0)  # max -> 999 999 999,99

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    @property
    def has_money(self):
        if self.account > 0:
            return True
        return False

    def __str__(self):
        return f'{self.username}: {self.inn}'
