from django.contrib import admin
from .models import ProviderProduct


@admin.register(ProviderProduct)
class ProviderProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'provider_device']
    exclude = ('booking', 'count', 'moderation', 'up_price', 'day_next_publish', 'name_tmp', 'device_provider', 'provider_device ')
