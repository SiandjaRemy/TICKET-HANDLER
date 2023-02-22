from django.contrib import admin
from .models import Profile, Category, Event, Order, Cart, QrInfo, Stadium, Guest, GuestOrder

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "id_user", "profile_approuved" ,"location"]
    list_editable = ('profile_approuved',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_going_on', 'created_at','updated_at')
    list_editable = ('slug', 'is_going_on')
    list_filter = ('is_going_on',)
    list_per_page = 10
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title", )}


class StadiumAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'location')
    list_per_page = 10
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date_time', 'category','is_active',  "available_tickets", 'slug', 'event_image', 'created_at', 'updated_at')
    list_editable = ('slug', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    list_per_page = 10
    search_fields = ('title', 'category')
    prepopulated_fields = {"slug": ("title", )}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'event')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket_checked', 'quantity', "date_passed", 'ordered_date')
    list_editable = ('quantity', 'ticket_checked')
    list_filter = ('ordered_date',)
    list_per_page = 20
    search_fields = ('user', 'event')

class GuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'age', 'id_card_number')
    list_per_page = 20

class GuestOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'guest_name', 'event', 'ticket_checked', 'quantity', "date_passed", 'ordered_date')
    list_editable = ('quantity', 'ticket_checked')
    list_filter = ('ordered_date',)
    list_per_page = 20
    search_fields = ('user', 'event')

class QrInfoAdmin(admin.ModelAdmin):
    list_display = ["code", "attributed", "qr_image", "created_on"]
    list_editable = ('attributed',)



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stadium, StadiumAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(GuestOrder, GuestOrderAdmin)
admin.site.register(QrInfo, QrInfoAdmin)
