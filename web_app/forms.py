"""
References:
    CreateAccountForm based on 'LogMessageForm' in 'use the database through the models' section of Django tutorial:

    Visual Studio Code (2023) [online] Python and Django tutorial in Visual Studio Code. Available at:
    https://code.visualstudio.com/docs/python/tutorial-django (Accessed: 13 July 2023).

    RegisterEngineerForm based on 'create the register form' found at:

    Ordinary Coders (2020) [online] A Guide to User Registration, Login, and Logout in Django. Available at:
    https://ordinarycoders.com/blog/article/django-user-register-login-logout (Accessed: 13 July 2023).

    SetTestingStatusForm based on the comment by Chad on Stack Overflow:

    Chad (2021) [online] ‘Django dropdown menu/form based on model entries’, Stack Overflow. Available at:
    https://stackoverflow.com/questions/66655712/django-dropdown-menu-form-based-on-model-entries
    (Accessed: 13 July 2023).
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from web_app.models import Account, Engineer


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("ASIN", "marketplace", "description", "status")


class EditAccountForm(forms.ModelForm):
    ASIN = forms.CharField(disabled=True)
    created = forms.DateTimeField(disabled=True)

    class Meta:
        model = Account
        fields = ("ASIN", "created", "marketplace", "description", "status")


class RegisterEngineerForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Register'))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "is_superuser")

    def save(self, commit=True):
        user = super(RegisterEngineerForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        engineer = Engineer()
        engineer.name = user.get_full_name()
        if commit:
            engineer.save()
            user.save()
        return user


class SetTestingStatusForm(forms.Form):
    engineer = forms.ModelChoiceField(
        label="Engineer Choices", queryset=Engineer.objects.all(), required=True)
