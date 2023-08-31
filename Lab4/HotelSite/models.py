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
    client_data = models.OneToOneField(ClientData, on_delete=models.CASCADE, blank=True, related_name='client')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ClientManager()

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.patronymic


class RoomType(models.Model):
    name = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.name

class Room(models.Model):
    description = models.CharField(max_length=400, blank=True)
    photo = models.ImageField(blank=True, upload_to='images/')
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=12)
    capacity = models.IntegerField(blank=True)
    room_type = models.OneToOneField(RoomType, on_delete=models.CASCADE, blank=True)

class Booking(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, blank=True, related_name='booking')
    room = models.OneToOneField(Room, on_delete=models.CASCADE, blank=True, related_name='booking')
    entry_date = models.DateTimeField(blank=True)
    departure_date = models.DateTimeField(null=True,blank=True)