from django.shortcuts import render
from actionplans import actions


def actionplans(request):

    return render(request, 'action_plan.html', {'listOfActions': actions})