from django.contrib import admin

from .models import TradeInStepModel, VariableFoeStepModel, \
    TradeInSeriesModel, \
    TradeInDevicesModel, \
    UserStepModel, \
    TelegramUserModel


# @admin.register(TelegramUserModel)
# class TelegramUserModelAdmin(admin.ModelAdmin):
#     pass


# @admin.register(UserStepModel)
# class UserStepModelAdmin(admin.ModelAdmin):
#     pass


@admin.register(TradeInSeriesModel)
class TradeInSeriesModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TradeInDevicesModel)
class TradeInDevicesModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TradeInStepModel)
class TradeInStepModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'step', 'series']



@admin.register(VariableFoeStepModel)
class VariableFoeStepModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'increase', 'decrease', 'step', ]
