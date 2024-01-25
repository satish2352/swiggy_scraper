from django.contrib import admin
from django.urls import path
from .views import scrap_swiggy_data, successfully_scrap


urlpatterns = [
    path('scrapdata/',successfully_scrap,name='scrapdata'),
    path('', scrap_swiggy_data,name=''),
]
