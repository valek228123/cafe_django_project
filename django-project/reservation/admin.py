from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(ModelAdmin):
    list_display = ['user',"table__number","date"]
    list_filter = ['date',"user"]
    search_fields = ['user__username','table__number',"date"]
    date_hierarchy = "date"
    list_select_related = ["user","table"]
    readonly_fields = ["date"]
    list_per_page = 25