from django.shortcuts import render
from Nile_App.models import CarbonIndustry, CarbonCompany, UserDetails
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
        scope1 = CarbonCompany.objects.filter(company_name=com_name).filter(year=y).filter(
            scope=1).first().total_emissions
        scope2 = CarbonCompany.objects.filter(company_name=com_name).filter(year=y).filter(
            scope=2).first().total_emissions
        scope3 = CarbonCompany.objects.filter(company_name=com_name).filter(year=y).filter(
            scope=3).first().total_emissions
        total = scope1 + scope2 + scope3
        scope1_list.append(json.loads(json.dumps(scope1, cls=DjangoJSONEncoder)))
        scope2_list.append(json.loads(json.dumps(scope2, cls=DjangoJSONEncoder)))
        scope3_list.append(json.loads(json.dumps(scope3, cls=DjangoJSONEncoder)))
        emissions_list.append(json.loads(json.dumps(total, cls=DjangoJSONEncoder)))
    # get cost list and cost and total emissions for the most recent year
    cost_list = [json.loads(json.dumps(get_carbon_cost(t), cls=DjangoJSONEncoder)) for t in emissions_list]
    cost = cost_list[-1]
    total_emissions = emissions_list[-1]
    # finally get industry and compary with avg for industry
    industry = CarbonCompany.objects.filter(company_name=com_name).first().industry
    industry_avg = 2.78
    industry_avg_list = [3.68, 3.66, 2.58, 4.32, 7.22, 8.25]
    # FIRST GRAPH: Multibar Chart of Carbon over years, by scope
    xdata = year_list
    ydata1 = scope1_list
    ydata2 = scope2_list
    ydata3 = scope3_list
    extra_serie = {"tooltip": {"y_start": "", "y_end": " million tonnes"}}

    chartdata1 = {
        'x': xdata,
        'name1': 'Scope 1', 'y1': ydata1, 'extra1': extra_serie, 'kwargs1': { 'color': '#5d8aa8'},
        'name2': 'Scope 2', 'y2': ydata2, 'extra2': extra_serie, 'kwargs2': { 'color': '#e32636'},
        'name3': 'Scope 3', 'y3': ydata3, 'extra3': extra_serie, 'kwargs3': { 'color': '#efdecd'}
    }

    charttype1 = "lineChart"
    chartcontainer1 = 'multibarchart_container1'  # container name
    data = {
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

    # SECOND GRAPH: A split of this year's consumtion by scope
    xdata = ["Scope 1", "Scope 2", "Scope 3"]
    ydata = [scope1_list[-1], scope2_list[-1], scope3_list[-1]]
    color_list = ['#5d8aa8', '#e32636', '#efdecd']
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " million tonnes"},
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
    # GRAPH THREE: A year-by-year comparison of the usage vs industry avg
    xdata = year_list
    ydata1 = industry_avg_list
    ydata2 = emissions_list
    extra_serie1 = {"tooltip": {"y_start": "$ ", "y_end": " million tonnes"}}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " million tonnes"}}
    chartdata3 = {
        'x': xdata,
        'name1': 'Industry Avg', 'y1': ydata1, 'extra1': extra_serie1, 'kwargs1': {'color': '#5d8aa8', 'bar': True},
        'name2': 'Your Eimssions', 'y2': ydata2, 'extra2': extra_serie2, 'kwargs2': {'color': '#e32636'},
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
    # Finally add it to the passed dictionary to the template
    data.update(data3)

    # FOURTH GRAPH: Plotting the Cost against years
    extra_serie = {"tooltip": {"y_start": "", "y_end": " thousand pounds"}}
    xdata = year_list
    ydata4 = cost_list
    chartdata4 = {
        'x': xdata,
        'name1': 'Annual Cost', 'y1': ydata4, 'kwargs1': {'color': '#5d8aa8'}
    }
    charttype4 = "multiBarChart"
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
    print('SCOPE 1: ', scope1_list)
    print('SCOPE 2: ', scope2_list)
    print('SCOPE 3: ', scope3_list)
    print('EMISSIONS_TOTAL: ', emissions_list)
    print('COST_LIST: ', cost_list)
    print('COST: ', cost)
    print(industry)
    data.update({'company': com_name, 'cost': cost, 'total_emissions': total_emissions})
    return render(request, 'carbon_dashboard.html', data)
