from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from Nile_App.forms import LoginForm
from actionplans import *


# Create your views here.

def index(request):
    login_form = LoginForm()
    return render(request, 'index.html', {'login_form': login_form})
