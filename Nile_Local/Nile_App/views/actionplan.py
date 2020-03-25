from django.shortcuts import render
from actionplans import actions


def index(request):
    return render(request, 'action_plan.html', {'listOfActions': actions})