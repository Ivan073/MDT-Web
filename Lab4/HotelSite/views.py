from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    context={"error":False}
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(views.home)
        context={"error":True}
    else:
        form = AuthenticationForm()
    return render(request, "login.html", context)

def signup_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(views.home)
    else:
        form = AuthenticationForm()
    return render(request, "signup.html")

def home_view(request):
    context={
        "user":request.user
    }
    return render(request, "home.html",context=context)
