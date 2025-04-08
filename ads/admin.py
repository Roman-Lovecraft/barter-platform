from django.contrib import admin
from users.models import ExchangeOffer

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'created_at')
    search_fields = ('name', 'description')

class ExchangeOfferAdmin(admin.ModelAdmin):
    list_display = ('item_offered', 'item_requested', 'offerer', 'status')
    list_filter = ('status',)
    search_fields = ('item_offered__name', 'item_requested__name')