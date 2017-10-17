#forms.py
import re
from Users.models import MyUser
from django import forms
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationForm(forms.Form):

    ADMIN='Admin'
    BOOKKEEPER='Bookkeeper'
    CASHIER='Cashier'

    POS = (
        (ADMIN, 'Admin'),
        (BOOKKEEPER, 'Bookkeeper'),
        (CASHIER, 'Cashier'),
    )

<<<<<<< HEAD
    first_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("First name"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    last_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Last name"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") }) 
=======
    first_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Firstname"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    last_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Lastname"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") }) 
>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    #email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=False, max_length=30, default='sample@yopmail.com')), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
    #position = forms.CharField(label='Position', max_length=50)
    position = forms.ChoiceField(
        choices=POS,
    )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        print self.cleaned_data['position']
        return self.cleaned_data

    # class Meta:
    #     model = MyUser

    # def clean_userpic(self):
    #     userpic = self.cleaned_data['userpic']

    #     try:
    #         w, h = get_image_dimensions(userpic)

    #         #validate dimensions
    #         max_width = max_height = 100
    #         if w > max_width or h > max_height:
    #             raise forms.ValidationError(
    #                 u'Please use an image that is '
    #                  '%s x %s pixels or smaller.' % (max_width, max_height))

    #         #validate content type
    #         main, sub = userpic.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError(u'Please use a JPEG, '
    #                 'GIF or PNG image.')

    #         #validate file size
    #         if len(userpic) > (20 * 1024):
    #             raise forms.ValidationError(
    #                 u'userpic file size may not exceed 20k.')

    #     except AttributeError:
    #         """
    #         Handles case when we are updating the user profile
    #         and do not supply a new userpic
    #         """
    #         pass

    #     return userpic

        
# class ClientsForm(forms.Form):
#     first_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Firstname"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
#     last_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Lastname"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })


