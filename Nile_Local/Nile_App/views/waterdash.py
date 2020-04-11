from django.shortcuts import render
from Nile_App.models import WaterIndustry, WaterCompany, UserDetails
import json
from django.core.serializers.json import DjangoJSONEncoder
from dashboard_calculations import *


def dashboard(request):
    # Get all DB entries for the company the user works at
    user_details = UserDetails.objects.get(user_id=request.user.id)
    com_name = user_details.company_name
    entries = WaterCompany.objects.filter(company_name=com_name).order_by('year')
    year_list = [e.year for e in entries]
    usage_list = [get_water_consum(e.no_of_employees) for e in entries]
    # This return a list of tuples: where the first item is the cost for this year and the second is a dictionary
    # holding the cheaper suppliers and their rates
    costsupp_list = [get_water_cost(e.no_of_employees, e.supplier) for e in entries]
    # Now split into cost list and suppliers dictionary, I am only using the latest years' suppliers rates since for
    # my specific data found all year are the same
    cost_list = [x[0] for x in costsupp_list]
    cost = cost_list[-1]
    recommended_supp_dicts = costsupp_list[-1][-1]
    # Now for the comparison against industry, I need to get the first instance only since it is the same industry
    # every year, then compare it with the rate for the same industry in the latest year, ideally should've been the
    # same year but 2020 data is not available yet'
    industry = WaterCompany.objects.filter(company_name=com_name).first().industry
    # let industry avg be equal this arbitrary value for testing now till actual data is found
    industryavg = 39971840000000
    # This is a one-off example on how I tested queryset outcomes
    print('TESTING YEARS:', year_list)
    print('TESTING CONSUMPTION:', usage_list)
    print('TESTING TUPLES', costsupp_list)
    print('TESTING COST', cost_list)
    print('TESTING RECOMMENDED SUPPLIERS', recommended_supp_dicts)
    print(industry)
    data = {'company': com_name}
    return render(request, 'water_dashboard.html', data)
