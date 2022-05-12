from django.contrib import admin
from .models import ButtonModel, ServiceModels,UserChoiceModel,UseService

@admin.register(ButtonModel)
class ButtonModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceModels)
class ServiceModelsAdmin(admin.ModelAdmin):
    pass

@admin.register(UserChoiceModel)
class UserChoiceModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UseService)
class UseServiceAdmin(admin.ModelAdmin):
    pass
