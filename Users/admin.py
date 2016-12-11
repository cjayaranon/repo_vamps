from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import MyUser
from django.contrib.auth.forms import UserChangeForm


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser


class UserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password','position', 'userpic')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'position','userpic')
        }
        ),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ['username', 'first_name', 'last_name']

#admin.site.register(User, UserAdmin)
admin.site.register(MyUser, UserAdmin)