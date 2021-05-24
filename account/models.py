from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    inn = models.CharField(
        _("ИНН"),
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex='^\d{10}$', message='Should be 10 digits number')],
    )
    account = models.FloatField(_("Счет"), default=0)

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f'{self.username}: {self.inn}'
