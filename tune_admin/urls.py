from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import bot
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('v1', bot)

]
