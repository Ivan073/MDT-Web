from django.contrib import admin
from .models import Client, ClientData, Room, RoomType, Booking

admin.site.register(Client)
admin.site.register(ClientData)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Booking)
