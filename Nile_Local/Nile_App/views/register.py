from django.shortcuts import render
from Nile_App.forms import UserForm, UserDataForm, LoginForm

# Create logic for registration pages here

def registration(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserDataForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            new_password = user_form.cleaned_data['password1']
            user.set_password(new_password)
            user.save()
            profile = profile_form.save(commit=False)

            # Set One to One relationship between user and their extra details
            profile.user = user
            profile.save()
            registered = True
            return render(request, 'registration.html', {'registered': registered})
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Unbound forms (not completed)
        user_form = UserForm()
        profile_form = UserDataForm()

    return render(request, 'registration.html', {'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 'registered': registered})



