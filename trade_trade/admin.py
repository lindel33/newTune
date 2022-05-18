from django.contrib import admin

from .models import Trade

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    pass

