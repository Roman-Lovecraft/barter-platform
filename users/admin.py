# filepath: c:\python\barter-platform\users\admin.py
from django.contrib import admin
from users.models import ExchangeOffer

@admin.register(ExchangeOffer)
class ExchangeOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')