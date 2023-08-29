import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout
from django import forms
from .models import Client, ClientData
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin

logger = logging.getLogger(__name__)


class ClientAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')

    def get_user(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = Client.objects.get(email=email)
        if user.check_password(password):
            return user

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
def login_view(request):
    context={"error":False}
    if request.method == "POST":
        form = ClientAuthenticationForm(request, request.POST)
        logger.warning("test")
        if form.is_valid():
            user = form.get_user()
            if user is None:
                context = {"error": True}
                return render(request, "login.html", context)
            login(request, user)
            return redirect(home_view)
        context={"error": True, "errors":form.errors}
    return render(request, "login.html", context)

class CustomUserCreation(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Client
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'patronymic']

    def save(self, commit=True):
        user = super().save(commit=False)
        client_data = ClientData.objects.create(info='', has_child=False)
        if commit:
            user.client_data = client_data
            user.save()
        return user


def signup_view(request):
    context = {"error": False}
    if request.method == "POST":
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(home_view)
        context = {"error": True, "errors":form.errors}
    return render(request, "signup.html",context)

def home_view(request):
    context={
        "user":request.user
    }
    return render(request, "home.html",context=context)

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))