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
    current_usage = rec_list[-1] + unrec_list[-1]
    total_amount_list = []
    print(len(rec_list))
    for n in range(len(rec_list)):
        tonnes = Decimal(rec_list[n]) + Decimal(unrec_list[n])
        cost_list.append(json.loads(json.dumps(get_waste_cost(tonnes), cls=DjangoJSONEncoder)))
        total_amount_list.append(json.loads(json.dumps(tonnes, cls=DjangoJSONEncoder)))



    cost = cost_list[-1]
    industry = WasteCompany.objects.filter(company_name=com_name).first().industry
    ind_average_list = [59000, 61233, 55333, 59870, 69888, 62198, 54967]
    print('TESTING YEARS:', year_list)
    print('TESTING RECYCLED:', rec_list, rec_amount)
    print('TESTING RECYCLED:', unrec_list, unrec_amount)
    print('TESTING Total Usage:', total_amount_list)
    print('TESTING COST', cost_list)
    print('TESTING CURRENT COST', cost)
    print(industry)
    data = {'company': com_name, 'cost': cost, 'usage': current_usage}

    # FIRST GRAPH: Multibar Chart of Waste over years, by type (recycled/unrecycled)
    xdata = year_list
    ydata1 = rec_list
    ydata2 = unrec_list
    extra_serie = {"tooltip": {"y_start": "", "y_end": " tonnes"}}

    chartdata1 = {
        'x': xdata,
        'name1': 'Recycled Amount', 'y1': ydata1, 'extra1': extra_serie, 'kwargs1': {'color': '#2F4F4F'},
        'name2': 'Unrecycled Amount', 'y2': ydata2, 'extra2': extra_serie, 'kwargs2': {'color': '#228B22'},
    }

    charttype1 = "multiBarChart"
    chartcontainer1 = 'multibarchart_container1'  # container name
    data1 = {
        'charttype1': charttype1,
        'chartdata1': chartdata1,
        'chartcontainer1': chartcontainer1,
        'extra1': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
    }

    # Add the data to the passes in template variables
    data.update(data1)

    # SECOND GRAPH: A split of this year's consumtion by type of waste
    xdata = ["Recycled Amount", "Unrecycled Amount"]
    ydata = [rec_list[-1], unrec_list[-1]]
    color_list = ['#228B22', '#004E59']
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " tonnes"},
        "color_list": color_list
    }
    chartdata2 = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype2 = "pieChart"
    chartcontainer2 = 'piechart_container2'  # container name

    data2 = {
        'charttype2': charttype2,
        'chartdata2': chartdata2,
        'chartcontainer2': chartcontainer2,
        'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'donut': True,
            'donutRatio': 0.35,
            'chart_attr': {
                'labelThreshold': 0.5,
                'labelType': '\"percent\"',
            }
        }
    }
    # Finally add it to the passed dictionary to the template
    data.update(data2)

    # GRAPH THREE: A year-by-year comparison of the waste amounts total vs industry avg
    xdata = year_list
    ydata1 = ind_average_list
    ydata2 = total_amount_list
    extra_serie1 = {"tooltip": {"y_start": "$ ", "y_end": " tonnes"}}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " tonnes"}}
    chartdata3 = {
        'x': xdata,
        'name1': 'Industry Avg', 'y1': ydata1, 'extra1': extra_serie1, 'kwargs1': {'color': '#2F4F4F', 'bar': True},
        'name2': 'Your Total Amount', 'y2': ydata2, 'extra2': extra_serie2, 'kwargs2': {'color': '#004E59'},
    }

    charttype3 = "linePlusBarChart"
    chartcontainer3 = 'lineplusbarchart_container3'  # container name
    data3 = {
        'charttype3': charttype3,
        'chartdata3': chartdata3,
        'chartcontainer3': chartcontainer3,
        'extra3': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'focus_enable': True,
        },
    }
    # # Finally add it to the passed dictionary to the template
    data.update(data3)

    # FOURTH GRAPH: Plotting the Cost against years
    extra_serie = {"tooltip": {"y_start": "", "y_end": " thousand pounds"}}
    xdata = year_list
    ydata4 = cost_list
    chartdata4 = {
        'x': xdata,
        'name1': 'Annual Cost', 'y1': ydata4, 'kwargs1': {'color': '#004E59'}
    }
    charttype4 = "lineChart"
    chartcontainer4 = 'linechart_container4'  # container name
    data4 = {
        'charttype4': charttype4,
        'chartdata4': chartdata4,
        'chartcontainer4': chartcontainer4,
        'extra4': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        }
    }
    # Finally add it to the passed dictionary to the template
    data.update(data4)
    return render(request, 'waste_dashboard.html', data)