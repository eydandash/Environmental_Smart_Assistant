from django.shortcuts import render
from Nile_App.models import CarbonIndustry,CarbonCompany,UserDetails
import json
from django.core.serializers.json import DjangoJSONEncoder
from dashboard_calculations import *

def dashboard(request):
    # Get all DB entries for the company the user works at
    user_details = UserDetails.objects.get(user_id=request.user.id)
    com_name = user_details.company_name
    entries = CarbonCompany.objects.filter(company_name=com_name).order_by('year')
    # gett years
    year_list = list(set(e.year for e in entries))
    year_list.sort()
    # get a list of total_emisions, which are the sum of the 3 scope per year
    scope1_list = []
    scope2_list = []
    scope3_list = []
    emissions_list = []
    for y in year_list:
        scope1 = CarbonCompany.objects.filter(company_name=com_name).filter(year=y).filter(scope=1).first().total_emissions
        scope2 = CarbonCompany.objects.filter(company_name=com_name).filter(year=y).filter(scope=1).first().total_emissions
        scope3 = CarbonCompany.objects.filter(company_name=com_name).filter(year=y).filter(scope=3).first().total_emissions
        total = scope1 + scope2 + scope3
        scope1_list.append(json.loads(json.dumps(scope1, cls=DjangoJSONEncoder)))
        scope2_list.append(json.loads(json.dumps(scope2, cls=DjangoJSONEncoder)))
        scope3_list.append(json.loads(json.dumps(scope3, cls=DjangoJSONEncoder)))
        emissions_list.append(json.loads(json.dumps(total, cls=DjangoJSONEncoder)))
    # get cost list and cost for the most recent year
    cost_list = [json.loads(json.dumps(get_carbon_cost(t), cls=DjangoJSONEncoder)) for t in emissions_list]
    cost = cost_list[-1]
    # finally get industry and compary with avg for industry
    industry = CarbonCompany.objects.filter(company_name=com_name).first().industry
    industry_avg = 2.78
    print('SCOPE 1: ', scope1_list)
    print('SCOPE 2: ', scope2_list)
    print('SCOPE 3: ', scope3_list)
    print('EMISSIONS_TOTAL: ', emissions_list)
    print('COST_LIST: ', cost_list)
    print('COST: ', cost)
    print(industry)
    data = {'company': com_name}
    return render(request, 'carbon_dashboard.html', data)
