from django.contrib import admin
from .models import Global, Iphone, Markup, Ipad, MacBook1, Watch, SpecialCharacter
from cost_models.models import DetailModel


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    pass


@admin.register(MacBook1)
class MacBookAdmin(admin.ModelAdmin):
    pass


@admin.register(Ipad)
class IpadAdmin(admin.ModelAdmin):
    pass

@admin.register(Global)
class GlobalAdmin(admin.ModelAdmin):
    pass


@admin.register(Iphone)
class IphoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Markup)
class MarkupAdmin(admin.ModelAdmin):
    pass


@admin.register(SpecialCharacter)
class SpecialCharacterAdmin(admin.ModelAdmin):
    list_display = ['provider_variant', 'new_variant', ]
