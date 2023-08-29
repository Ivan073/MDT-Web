from . import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('signup', views.signup_view),
    path('admin', admin.site.urls),
]