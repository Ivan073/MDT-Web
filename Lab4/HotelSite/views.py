import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout
from .models import Client, ClientData, Room, RoomType, Booking, Payment, Article, Vacancy, Promocode, Review, FAQ
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin
from .forms import ClientAuthenticationForm, ClientCreationForm
import requests
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

logger = logging.getLogger(__name__)

def login_view(request):
    logger.info("Login page")
    context={"error":False}
    if request.method == "POST":
        form = ClientAuthenticationForm(request, request.POST)

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
    logger.info("Signup page")
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

        unprocessed_errs = form.errors.as_data()
        errors = []
        if unprocessed_errs.get("email") is not None:
            for err in unprocessed_errs.get("email"):
                if err.code == 'unique':
                    errors.append("Пользователь с этим email уже зарегистрирован")
                if err.code == 'invalid':
                    errors.append("Введите корректный email")


        if unprocessed_errs.get("password2") is not None:
            for err in unprocessed_errs.get("password2"):
                if err.code == 'password_mismatch':
                    errors.append("Пароли не совпадают")

        logger.warning("Signup errors:"+str(errors))
        context["errors"] = errors
    return render(request, "signup.html",context)

def home_view(request):
    logger.info("Home page")
    rooms = Room.objects.all()
    if request.method == "POST":
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

        date = request.POST.get("date")

        if date is not None and date != '':
            date = datetime.strptime(date, '%Y-%m-%d')
            logger.warning(date)
            rooms = rooms.filter(free_date__lte=date)


    context={
        "user":request.user,
        "rooms":rooms,
        "amount":len(rooms),
        "tomorrow":datetime.today()+timedelta(days=1),
        "max": datetime.today() + timedelta(days=31)
    }
    try:
        context['article'] = Article.objects.all().order_by('-created_at')[0].heading
    except:
        pass
    return render(request, "home.html", context=context)

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def geo_view(request):
    logger.info("Place page")
    ip_response = requests.get('https://api.ipify.org/?format=json')
    ip = ip_response.json()['ip']
    logger.info('User IP: '+ip+" User name: ")
    place_responce = requests.get('https://ipinfo.io/'+ip+'/geo')
    place = place_responce.json()
    context = {'ip':ip,
               'postal':place['postal'],
               'city':place['city']}

    return render(request, "place.html",context=context)

def room_view(request, id):
    logger.info("Room "+str(id)+" page")
    room = Room.objects.get(id=id)
    return render(request, 'room.html', {'room': room, "user":request.user,"tomorrow":datetime.today()+timedelta(days=1),})

@login_required
def booking_view(request, id):
    logger.info("Booking room " + str(id) + " page")
    room = Room.objects.get(id=id)
    min_date = max(room.free_date,datetime.date(datetime.today()+timedelta(days=1)))
    max_date = min_date + timedelta(days=30)
    context = {'room': room,
               "user":request.user,
               "min_date":min_date,
               "max_date":max_date}
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        if start_date is not None and end_date is not None:
            start_date = datetime.date(datetime.strptime(start_date,'%Y-%m-%d'))
            end_date = datetime.date(datetime.strptime(end_date,'%Y-%m-%d'))
            if start_date <=  end_date:
                duration = (end_date-start_date).days+1
                context={"price":room.price*duration, "user":request.user,"room_id":id, "start_date":start_date,"end_date":end_date}
                request.session['price'] = float(room.price*duration)
                request.session['room_id'] = id
                request.session['start_date'] = str(start_date)
                request.session['end_date'] = str(end_date)
                logger.warning(context)
                return render(request, 'order.html', context)
            else:
                context["error"] = True
    return render(request, "booking.html",context)

@login_required
def payment_view(request):
    logger.info("Payment for room " + str(request.session['room_id']) + " page. Client: "+request.user.__str__())
    data = "Платеж проведен в "
    data+=str(datetime.now())
    data+=".\nСтоимость: "
    data+=str(request.session['price'])
    data+=".\nКлиент: "+request.user.__str__()
    Payment.objects.create(data=data);
    return redirect("/payment_finished")

@login_required
def payment_finsihed_view(request):
    logger.info("Finished payment page")
    Booking.objects.create(client=request.user,
                           room=Room.objects.get(id=request.session['room_id']),
                           entry_date=datetime.date(datetime.strptime(request.session['start_date'],'%Y-%m-%d')),
                           departure_date=datetime.date(datetime.strptime(request.session['end_date'],'%Y-%m-%d')))
    request.session.pop('price', None)
    request.session.pop('room_id', None)
    request.session.pop('start_date', None)
    request.session.pop('end_date', None)
    return render(request, "payment_successful.html")

@login_required
def bookings_view(request):
    logger.info("Own booking page. Client: " + request.user.__str__())
    bookings = Booking.objects.all().filter(client=request.user)
    return render(request, "bookings.html", {"user":request.user, "bookings":bookings})

@login_required
def statistics_view(request):
    logger.info("Statistics page")
    if not request.user.is_superuser:
        return redirect(home_view)
    rooms = Booking.objects.values('room').annotate(total_price=Sum('price')).order_by('-total_price')
    best_room = Room.objects.get(id=rooms[0]['room'])
    popular_room = Room.objects.get(
        id=(Booking.objects.values('room').annotate(count=Count('id')).order_by('-count')[0])['room']
    )
    graph_data = list(map(lambda x: list(x.values()), list(rooms)))
    graph_data = list(map(lambda x: ["Комната "+str(x[0]),float(x[1])],graph_data))

    booking_amount = len(Booking.objects.all())
    client_amount = len(Client.objects.all())
    room_amount = len(Room.objects.all())
    logger.warning(graph_data)
    context = {
        "user": request.user,
        "rooms_by_price": rooms,
        "best_room": best_room,
        "popular_room": popular_room,
        "graph_data":graph_data,
        'values': graph_data,
        'booking_amount':booking_amount,
        'client_amount': client_amount,
        'room_amount': room_amount,
    }

    return render(request, "statistics.html", context)

def terms_of_service_view(request):
    return render(request, "terms_of_service.html")

def vacancies_view(request):
    vacancies = Vacancy.objects.all()
    context = {"vacancies":vacancies}
    return render(request, "vacancies.html",context)

def promo_view(request):
    promocodes = Promocode.objects.all()
    active_promocodes = promocodes.filter(is_archived=False)
    inactive_promocodes = promocodes.filter(is_archived=True)
    context = {"active_promocodes": active_promocodes, "inactive_promocodes": inactive_promocodes}
    return render(request, "promocodes.html", context)

def reviews_view(request):
    reviews = Review.objects.all()
    context = {"reviews":reviews}
    return render(request, "reviews.html", context)

def faq_view(request):
    questions = FAQ.objects.all()
    context = {"questions":questions}
    return render(request, "FAQ.html", context)
