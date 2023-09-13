from django.contrib import admin
from .models import Client, ClientData, Room, RoomType, Booking, Payment, Article, Vacancy, Review

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'room', 'entry_date', 'departure_date', 'price')
    fields = ['client', 'room', ('entry_date', 'departure_date')]


class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'price', 'capacity','photo', 'free_date','room_type')


class ChildFilter(admin.SimpleListFilter):
    title = 'Есть ребенок'
    parameter_name = 'has_child'

    def lookups(self, request, model_admin):
        return (
            ('Да', 'Есть'),
            ('Нет', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Да':
            return queryset.filter(client_data__has_child=True)
        elif self.value() == 'Нет':
            return queryset.filter(client_data__has_child=False)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'has_child')
    list_filter = (ChildFilter,)

    def has_child(self, obj):
        if obj.client_data.has_child:
            return "Да"
        else:
            return "Нет"
    has_child.short_description = 'Есть ребенок'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'created_at')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'heading',  'created_at')

class VacancyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'rating', 'data')


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientData)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Review, ReviewAdmin)

from django.contrib.auth.models import Group
admin.site.unregister(Group)
