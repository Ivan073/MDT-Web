import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout
from .models import Client, ClientData, Room, RoomType
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin
from .forms import ClientAuthenticationForm, ClientCreationForm
import requests

logger = logging.getLogger(__name__)

def login_view(request):
    context={"error":False}
    if request.method == "POST":
        form = ClientAuthenticationForm(request, request.POST)
        logger.warning("test")
        if form.is_valid():
            user = form.get_user()
            if user is None:
                context = {"error": True, "email": request.POST["email"]}
                return render(request, "login.html", context)
            login(request, user)
            return redirect(home_view)
        context={"error": True}
    return render(request, "login.html", context)

def signup_view(request):

    context = {"error": False}

    if request.method == "POST":
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(home_view)
        context = {"error": True,
                   "email": request.POST["email"],
                   "last_name": request.POST["last_name"],
                   "first_name": request.POST["first_name"],
                   "patronymic": request.POST["patronymic"],
                   "info": request.POST["info"]}
        if request.POST.get("has_child") is not None:
            context["has_child"] = request.POST["has_child"]

        logger.warning(form.errors.as_data())
        unprocessed_errs = form.errors.as_data()
        errors = []
        if unprocessed_errs.get("email") is not None:
            for err in unprocessed_errs.get("email"):
                logger.warning(err.code)
                if err.code == 'unique':
                    errors.append("Пользователь с этим email уже зарегистрирован")
                if err.code == 'invalid':
                    errors.append("Введите корректный email")


        if unprocessed_errs.get("password2") is not None:
            for err in unprocessed_errs.get("password2"):
                logger.warning(err.code)
                if err.code == 'password_mismatch':
                    errors.append("Пароли не совпадают")

        logger.warning(errors)
        context["errors"] = errors
    return render(request, "signup.html",context)

def home_view(request):
    rooms = Room.objects.all()
    if request.method == "POST":
        logger.warning(request.POST)
        type_name = request.POST.get("type")
        if type_name is not None and type_name != '':
            type_obj = RoomType.objects.get(name=type_name)
            rooms = rooms.filter(room_type = type_obj)

        price_filter = request.POST.get("price_filter")
        price_radio = request.POST.get("price_radio")
        if price_filter is not None and price_filter != '':
            if price_radio == 'up':
                rooms = rooms.filter(price__gt=float(price_filter))
                rooms = rooms.order_by('price')
            elif price_radio == 'down':
                rooms = rooms.filter(price__lt=float(price_filter))
                rooms = rooms.order_by('-price')
            elif price_radio is None:
                rooms = rooms.filter(price=float(price_filter))

        capacity_filter = request.POST.get("capacity_filter")
        capacity_radio = request.POST.get("capacity_radio")
        if capacity_filter is not None and capacity_filter != '':
            if capacity_radio == 'up':
                rooms = rooms.filter(capacity__gt=float(capacity_filter))
            elif capacity_radio == 'down':
                rooms = rooms.filter(capacity__lt=float(capacity_filter))
            elif capacity_radio is None:
                rooms = rooms.filter(capacity=float(capacity_filter))
    logger.warning(rooms)
    context={
        "user":request.user,
        "rooms":rooms,
        "amount":len(rooms),
    }
    return render(request, "home.html",context=context)

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def geo_view(request):
    ip_response = requests.get('https://api.ipify.org/?format=json')
    ip = ip_response.json()['ip']
    logger.info('IP:'+ip)
    place_responce = requests.get('https://ipinfo.io/'+ip+'/geo')
    place = place_responce.json()
    context = {'ip':ip,
               'postal':place['postal'],
               'city':place['city']}
    logger.info(context)
    return render(request, "place.html",context=context)

def room_view(request, id):
    room = Room.objects.get(id=id)
    return render(request, 'room.html', {'room': room})