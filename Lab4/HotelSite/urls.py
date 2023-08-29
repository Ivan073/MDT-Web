from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('signup', views.signup_view),
]