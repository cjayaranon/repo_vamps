from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import MyUser


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser

@admin.register(MyUser)
class UserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'position',)
        }
        ),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissons')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'position', 'is_staff')
    search_fields = ("username", "first_name", "last_name", "email", "position")
    ordering = ("username",)