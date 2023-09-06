from django.contrib import admin
from .models import Client, ClientData, Room, RoomType, Booking, Payment

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'room', 'entry_date', 'departure_date', 'price')
    fields = ['client', 'room', ('entry_date', 'departure_date')]


class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'price', 'capacity','photo', 'free_date')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'has_child')

    def has_child(self, obj):
        if obj.client_data.has_child:
            return "Да"
        else:
            return "Нет"
    has_child.short_description = 'Есть ребенок'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'created_at')


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientData)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)

from django.contrib.auth.models import Group
admin.site.unregister(Group)
