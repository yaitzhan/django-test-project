from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'inn', 'account',)
    list_filter = ('username', 'inn', 'inn',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'inn', 'account')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'inn', 'account', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'inn')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
