from django.shortcuts import render
from Nile_App.models import  WaterCompany, UserDetails
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
    industryavg_list = [133, 324, 234, 456, 234, 432, 654, 664]

    data = {'company': com_name, 'suppliers_dict': recommended_supp_dicts, 'cost': cost}

    # FIRST GRAPH: Line chart for water consum over years
    xdata = year_list
    ydata1 = usage_list
    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}

    chartdata1 = {
        'x': xdata,
        'name1': 'Water Consumption', 'y1': ydata1, 'extra1': extra_serie, 'kwargs1': {'color': '#292b2c'},
    }
    charttype1 = "multiBarChart"
    chartcontainer1 = 'linechart_container1'  # container name
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
    # Now Update with the context passed into template
    data.update(data1)

    # GRAPH TWO: A year-by-year comparison of the usage vs industry avg
    xdata = year_list
    ydata1 = industryavg_list
    ydata2 = usage_list
    extra_serie1 = {"tooltip": {"y_start": "$ ", "y_end": ""}}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata2 = {
        'x': xdata,
        'name1': 'Industry Avg', 'y1': ydata1, 'extra1': extra_serie1, 'kwargs1': {'color': '#292b2c', 'bar': True},
        'name2': 'Your Consumption', 'y2': ydata2, 'extra2': extra_serie2, 'kwargs2': {'color': '#0275d8'},
    }
    charttype2 = "linePlusBarChart"
    chartcontainer2 = 'lineplusbarchart_container2'  # container name
    data2 = {
        'charttype2': charttype2,
        'chartdata2': chartdata2,
        'chartcontainer2': chartcontainer2,
        'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'focus_enable': True,
        },
    }
    # Finally add it to the passed dictionary to the template
    data.update(data2)

    # THIRD GRAPH: Line chart for water cost over years
    xdata = year_list
    ydata1 = cost_list
    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata3 = {
        'x': xdata,
        'name1': 'Water Cost', 'y1': ydata1, 'extra1': extra_serie, 'kwargs1': {'color': '#0275d8'},
    }
    charttype3 = "lineChart"
    chartcontainer3 = 'linechart_container3'  # container name
    data3 = {
        'charttype3': charttype3,
        'chartdata3': chartdata3,
        'chartcontainer3': chartcontainer3,
        'extra3': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
    }
    # Now Update with the context passed into template
    data.update(data3)

    # This is an example on how I tested queryset outcomes
    print('TESTING YEARS:', year_list)
    print('TESTING CONSUMPTION:', usage_list)
    print('TESTING TUPLES', costsupp_list)
    print('TESTING COST', cost_list)
    print('TESTING RECOMMENDED SUPPLIERS', recommended_supp_dicts)
    # print(industry)
    return render(request, 'water_dashboard.html', data)
