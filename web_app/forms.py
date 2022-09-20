from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from web_app.models import Customers, Engineers

class NewEngineerForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "is_superuser")

    def save(self, commit=True):
        user = super(NewEngineerForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user        

class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ("customerASIN",)   