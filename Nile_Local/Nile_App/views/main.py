from django.shortcuts import render
from django.http import HttpResponse
from actionplans import *



# Create your views here.

def index(request):
    # newone = Example.objects.create(e1="12cdsss")
    return render(request, 'action_plan.html', {'listOfActions': actions})

