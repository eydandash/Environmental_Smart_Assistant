# This file is created to contain different urls that will be used in the application views

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]