from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import ClientManager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ClientData(models.Model):
    info = models.CharField(max_length=400, blank=True)
    has_child = models.BooleanField(blank=True)
    def __str__(self):
        return "ClientData"+str(self.id)
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
    description = models.TextField(max_length=5000, blank=True)
    photo = models.ImageField(blank=True, upload_to='images/')
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=12)
    capacity = models.IntegerField(blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, blank=True)
    free_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return "Room"+str(self.id)

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, related_name='booking')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, related_name='booking')
    entry_date = models.DateField(blank=True)
    departure_date = models.DateField(null=True,blank=True)
    def __str__(self):
        return "Booking"+str(self.id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        logger.warning(self.room.free_date)
        logger.warning("0")
        if self.departure_date is not None:
            logger.warning("1")
            if self.departure_date > self.room.free_date:
                logger.warning("2")
                self.room.free_date = self.departure_date
        logger.warning(self.room.free_date)
        self.room.save(*args, **kwargs)
        super().save(*args, **kwargs)