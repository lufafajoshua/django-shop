from .models import User, Profile, UserAgent
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class CustomerSignUpForm(UserCreationForm):
    customer = Profile

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 1
        user.save()
        customer = Profile.objects.create(user=user)
        return user


class UserAgentSignUpForm(UserCreationForm):
    #availability = forms.BooleanField()
    #agent = Agent
    

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 3
        user.save()
        useragent = UserAgent.objects.get_or_create(user=user)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
