# This file is created to contain different urls that will be used in the application views

from django.urls import path

from Nile_App.views import *


urlpatterns = [
    path('', main.index, name='index'),
    path('registration/', register.registration, name='registration')
]
