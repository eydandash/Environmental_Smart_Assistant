from django.http import HttpResponseRedirect
from django.shortcuts import render
from Nile_App.forms import UserForm, UserDataForm, LoginForm


def registration(request):
    registered = False

    if request.method == 'POST':
        # if request.POST.get('submit') == 'sign_in':
        #     login_form = LoginForm(data=request.POST)
        #
        # elif request.POST.get('submit') == 'sign_up':
        user_form = UserForm(data=request.POST)
        profile_form = UserDataForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            new_password = user_form.cleaned_data['password1']
            user.set_password(new_password)
            user.save()
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            profile.user = user
            profile.save()
            registered = True

            return HttpResponseRedirect('generic_dashboard/')
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.cleaned_data['email'])
            print(user_form.cleaned_data['email2'])
            print(user_form.errors, profile_form.errors)
            login_form = LoginForm()
            return render(request, 'registration.html', {'login_form': login_form,
                                                         'user_form': user_form,
                                                         'profile_form': profile_form,
                                                         'registered': registered})
    # Unbound forms
    user_form = UserForm()
    profile_form = UserDataForm()
    login_form = LoginForm()
    return render(request, 'registration.html', {'login_form': login_form,
                                                 'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 'registered': registered})
