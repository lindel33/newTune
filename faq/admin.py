from django.contrib import admin
from .models import FAQModel


@admin.register(FAQModel)
class FAQModelAdmin(admin.ModelAdmin):
    pass
