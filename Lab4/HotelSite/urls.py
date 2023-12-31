from . import views
from django.urls import path, re_path
from django.contrib import admin

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('signup', views.signup_view),
    path('admin', admin.site.urls),
    path('place', views.geo_view),
    path('rooms/<int:id>/', views.room_view),
    path('booking/<int:id>/', views.booking_view),
    path('payment', views.payment_view),
    path('payment_finished', views.payment_finsihed_view),
    path('bookings', views.bookings_view),
    path('statistics', views.statistics_view),
]