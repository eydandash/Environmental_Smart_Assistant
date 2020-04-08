# This file is created to contain different urls that will be used in the application views

from django.urls import path

from Nile_App.views import *
from Nile_App.views import carbondash,wastedash,waterdash

urlpatterns = [
    path('', main.index, name='index'),
    path('registration/', register.registration, name='registration'),
    path('actionplan/', actionplan.actionplans, name='actionplan'),
    path('dashboard/', dashboards.dashboard, name='dashboard'),
    path('carbon_dashboard/', carbondash.dashboard, name='carbon_dashboard'),
    path('water_dashboard/', waterdash.dashboard, name='water_dashboard'),
    path('waste_dashboard/', wastedash.dashboard, name='waste_dashboard'),
]
