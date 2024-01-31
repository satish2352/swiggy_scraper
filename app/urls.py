from django.contrib import admin
from django.urls import path
from .views import scrap_swiggy_data, successfully_scrap,get_chart,chart_data2


urlpatterns = [
    path('scrapdata/',successfully_scrap,name='scrapdata'),
    path('', scrap_swiggy_data,name=''),
    path('chart1',get_chart,name='chart1'),
    path('chart2',chart_data2,name='chart2'),
]
