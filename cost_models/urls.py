from django.urls import path
from .views import index, not_update, ready


urlpatterns = [

    path('full/', index),
    path('ready/', ready),
    path('not_update/', not_update),
]
