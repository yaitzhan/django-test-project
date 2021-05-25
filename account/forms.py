from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)


class TransactionForm(forms.ModelForm):
    user_withdraw = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
                                           label='Пользователь (снятие)',
                                           required=True)
    users_replenish = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(),
                                                     label='Пользователи (пополнение)',
                                                     required=True)
    money_amount = forms.FloatField(label='Сумма', required=True)

    def clean(self):
        cleaned_data = super().clean()
        user_withdraw = cleaned_data.get("user_withdraw")
        users_replenish = cleaned_data.get("users_replenish")
        money_amount = cleaned_data.get("money_amount")

        if money_amount < 0:
            raise ValidationError(_('Money amount should be positive'), code='money_amount_negative')

        if user_withdraw.account - money_amount < 0:
            raise ValidationError(_(f'User: {user_withdraw} does not have enough money'), code='not_enough_money')

        if user_withdraw in users_replenish:
            raise ValidationError(_(f'Can not replenish to the same user'), code='user_circle_withdraw')

        return cleaned_data

    def process_transaction(self):
        cleaned_data = super().clean()
        user_withdraw = cleaned_data.get("user_withdraw")
        users_replenish = cleaned_data.get("users_replenish")
        money_amount = cleaned_data.get("money_amount")

        user_withdraw.account -= money_amount
        user_withdraw.save()

        money_amount_part = round(money_amount / users_replenish.count(), 2)

        # here we can use bulk-update-or-create approach for further optimizations
        for user in users_replenish:
            user.account += money_amount_part
            user.save()

    class Meta:
        model = CustomUser
        fields = ('user_withdraw', 'users_replenish', 'money_amount')

