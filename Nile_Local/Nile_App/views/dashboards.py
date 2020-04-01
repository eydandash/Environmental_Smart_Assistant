from django.shortcuts import render


def dashboard(request):
    return render(request, 'generic_dashboard.html')
