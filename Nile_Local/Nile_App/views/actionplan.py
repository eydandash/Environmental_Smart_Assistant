from django.shortcuts import render
from actionplans import actions
from Nile_App.models import UserDetails, User

def actionplans(request):
    print(request.user.id)
    user_details = UserDetails.objects.get(user_id=request.user.id)
    return render(request, 'action_plan.html', {'list_of_actions': actions, 'user_details': UserDetails})