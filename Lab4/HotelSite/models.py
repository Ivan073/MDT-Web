from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import ClientManager

# Create your models here.

class ClientData(models.Model):
    info = models.CharField(max_length=400, blank=True)
    has_child = models.BooleanField(blank=True)
class Client(AbstractUser):
    username = None
    email = models.EmailField(unique=True, primary_key=True)
    patronymic = models.CharField(max_length=100, blank=True)
    client_data = models.OneToOneField(ClientData, on_delete=models.CASCADE, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ClientManager()