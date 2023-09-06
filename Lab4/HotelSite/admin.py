from django.contrib import admin
from .models import Client, ClientData, Room, RoomType, Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'room', 'entry_date', 'departure_date', 'price')
    fields = ['client', 'room', ('entry_date', 'departure_date')]


class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'price', 'capacity','photo', 'free_date')


admin.site.register(Client)
admin.site.register(ClientData)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Booking, BookingAdmin)
