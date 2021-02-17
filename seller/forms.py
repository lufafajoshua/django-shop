from user_profiles.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Seller


class SellerSignUpForm(UserCreationForm):
    email = forms.EmailField()
    telephone = forms.CharField()
    country = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 2
        user.save()
        agent = Seller.objects.create(user=user)
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
