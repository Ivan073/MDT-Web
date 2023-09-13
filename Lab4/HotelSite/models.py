from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import ClientManager
from datetime import datetime, timedelta
import logging
from django.core.validators import MinValueValidator, MaxValueValidator

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
        return "Бронь "+str(self.id)

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

class Payment(models.Model):
    data = models.TextField(max_length=5000, blank=True, verbose_name="Содержимое")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return "Платеж " + str(self.id)

    class Meta:
        verbose_name_plural = 'Платежи'

class Article(models.Model):
    heading = data = models.TextField(max_length=200, blank=True, verbose_name="Заголовок")
    short_data = models.TextField(max_length=1000, blank=True, verbose_name="Краткое содержимое")
    data = models.TextField(max_length=5000, blank=True, verbose_name="Содержимое")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return "Статья " + str(self.id)

    class Meta:
        verbose_name_plural = 'Статьи'

class Vacancy(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="Название")
    info = models.TextField(max_length=5000, blank=True, verbose_name="Информация")

    def __str__(self):
        return "Вакансия " + str(self.id)

    class Meta:
        verbose_name_plural = 'Вакансии'

class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, related_name='review', verbose_name="Клиент")
    data = models.TextField(max_length=5000, blank=True, verbose_name="Содержимое")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return "Отзыв " + str(self.id)

    class Meta:
        verbose_name_plural = 'Отзывы'

class Promocode(models.Model):
    code = models.CharField(max_length=50, blank=True, verbose_name="Код")
    info = models.TextField(max_length=1000, blank=True, verbose_name="Информация")
    is_archived = models.BooleanField(blank=True, verbose_name="В архиве")

    def __str__(self):
        return "Промокод " + str(self.id)

    class Meta:
        verbose_name_plural = 'Промокоды'

class FAQ(models.Model):
    question = models.CharField(max_length=500, blank=True, verbose_name="Вопрос")
    answer = models.TextField(max_length=5000, blank=True, verbose_name="Ответ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return "Вопрос " + str(self.id)

    class Meta:
        verbose_name_plural = 'Часто задаваемые вопросы'