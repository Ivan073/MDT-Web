import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin

logger = logging.getLogger(__name__)
def login_view(request):
    context={"error":False}
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        logger.warning("test")
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(home_view)
        context={"error":True}
    return render(request, "login.html", context)

class CustomUserCreation(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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