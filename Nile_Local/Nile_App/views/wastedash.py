from django.shortcuts import render
from Nile_App.models import WasteCompany, WasteIndustry, UserDetails
import json
from django.core.serializers.json import DjangoJSONEncoder
from dashboard_calculations import *

def dashboard(request):
    # Get all DB entries for the company the user works at
    user_details = UserDetails.objects.get(user_id=request.user.id)
    com_name = user_details.company_name
    entries = WasteCompany.objects.filter(company_name=com_name).order_by('year')
    # get all years, set is used here to remove dupes since in the DB every year has two entires: recycled &
    # unrecycled, I have to sort them afterwards since sets are unordered structures in python
    year_list = list(set(e.year for e in entries))
    year_list.sort()
    recycled_queryset = WasteCompany.objects.filter(company_name=com_name).order_by('year').filter(type='recycled').values_list('amount', flat= True)
    unrecycled_queryset = WasteCompany.objects.filter(company_name=com_name).order_by('year').filter(type='unrecycled').values_list('amount', flat= True)
    # get list of recycled over years, and the recycked amount only for the reporting period (most recent year),
    # since amounts are all in deciaml JSON encoders have to be used
    rec_list = []
    unrec_list = []
    for x in recycled_queryset:
        y = json.dumps(x, cls=DjangoJSONEncoder)
        rec_list.append(json.loads(y))

    for x in unrecycled_queryset:
        y = json.dumps(x, cls=DjangoJSONEncoder)
        unrec_list.append(json.loads(y))

    rec_amount = rec_list[-1]
    unrec_amount = unrec_list[-1]
    # get cost for the latest year by summing total tonnes from rec+unrec, and compare it with industry avg,
    # assigned arbitrarily
    cost_list = []
    print(len(rec_list))
    for n in range(len(rec_list)):
        tonnes = Decimal(rec_list[n]) + Decimal(unrec_list[n])
        cost_list.append(json.loads(json.dumps(get_waste_cost(tonnes), cls=DjangoJSONEncoder)))
        print(tonnes)

    cost = cost_list[-1]
    industry = WasteCompany.objects.filter(company_name=com_name).first().industry
    ind_avg = 37373738.00
    print('TESTING YEARS:', year_list)
    print('TESTING RECYCLED:', rec_list, rec_amount)
    print('TESTING RECYCLED:', unrec_list, unrec_amount)
    print('TESTING COST', cost_list)
    print('TESTING CURRENT COST', cost)
    print(industry)
    data = {'company': com_name}
    return render(request, 'waste_dashboard.html', data)