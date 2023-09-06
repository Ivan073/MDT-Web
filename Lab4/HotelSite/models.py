from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import ClientManager
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ClientData(models.Model):
    info = models.CharField(max_length=400, blank=True, verbose_name="Информация")
    has_child = models.BooleanField(blank=True, verbose_name="Есть ребенок")
    def __str__(self):
        return "ClientData"+str(self.id)

    class Meta:
        verbose_name_plural = 'Данные клиентов'
class Client(AbstractUser):
    username = None
    email = models.EmailField(unique=True, primary_key=True)
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    client_data = models.OneToOneField(ClientData, on_delete=models.CASCADE, blank=True, related_name='client', verbose_name="Данные клиента")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ClientManager()

    class Meta:
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.patronymic


class RoomType(models.Model):
    name = models.CharField(max_length=50, blank=True, verbose_name="Название")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Типы комнат'

class Room(models.Model):
    description = models.TextField(max_length=5000, blank=True, verbose_name="Описание")
    photo = models.ImageField(blank=True, upload_to='images/', verbose_name="Фото")
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=12, verbose_name="Цена")
    capacity = models.IntegerField(blank=True, verbose_name="Вместимость")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, blank=True, verbose_name="Тип комнаты")
    free_date = models.DateField(blank=True, null=True, verbose_name="Свободна с")

    class Meta:
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return "Комната "+str(self.id)

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, related_name='booking', verbose_name="Клиент")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, related_name='booking', verbose_name="Комната")
    entry_date = models.DateField(blank=True, verbose_name="Дата въезда")
    departure_date = models.DateField(null=True,blank=True, verbose_name="Дата выезда")
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=12, editable=False, default=0, verbose_name="Стоимость")
    def __str__(self):
        return "Booking"+str(self.id)

    class Meta:
        verbose_name_plural = 'Брони'

    def save(self, *args, **kwargs):
        self.price = self.room.price * (self.departure_date-self.entry_date+timedelta(days=1)).days
        super().save(*args, **kwargs)
        if self.departure_date is not None:
            if self.departure_date >= self.room.free_date:
                self.room.free_date = self.departure_date + timedelta(days=1)
        logger.warning(self.room.free_date)
        self.room.save(update_fields=["free_date"])