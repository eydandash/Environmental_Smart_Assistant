import datetime
import random
import time

from django.shortcuts import render
from Nile_App.models import CarbonIndustry, WaterIndustry, WasteIndustry, UserDetails
import json
from django.core.serializers.json import DjangoJSONEncoder


def dashboard(request):
    # First GRAPH, to compare carbon_intensity per industry per year LINE CHART, Since maps are not subscriptable, I had to format all of the maps which return a map
    # to a list to use the, in graphs. Using maps as included in the official NVD3 Django documentation didn't work.
    # PLEASE NOTE: ind = industry, y = year, ci = carbon intensity
    # The serializer and deserializer, keep failing to convert Decimal types into any JSON identifiable format.
    years_list_carbon = CarbonIndustry.objects.all().values_list('year', flat=True).distinct().order_by('year')
    industries_list = CarbonIndustry.objects.all().values_list('industry', flat=True).distinct()
    intensities_list = []
    intensities_list2 = []
    intensities_list3 = []
    for x in CarbonIndustry.objects.filter(industry="Manufacturing").values_list('intensity', flat=True):
        y = json.dumps(x, cls=DjangoJSONEncoder)
        intensities_list.append(json.loads(y))

    for x in CarbonIndustry.objects.filter(industry="Transport and storage").values_list('intensity', flat=True):
        y = json.dumps(x, cls=DjangoJSONEncoder)
        intensities_list2.append(json.loads(y))

    for x in CarbonIndustry.objects.filter(industry="Construction").values_list('intensity', flat=True):
        y = json.dumps(x, cls=DjangoJSONEncoder)
        intensities_list3.append(json.loads(y))
    xdata_carbon = years_list_carbon
    ydata_carbon = intensities_list
    ydata2_carbon = intensities_list2
    ydata3_carbon = intensities_list3
    chartdata_carbon = {
        'x': xdata_carbon,
        'name1': 'Manufacturing', 'y1': ydata_carbon,
        'name2': 'Transport and Storage', 'y2': ydata2_carbon,
        'name3': 'Construction', 'y3': ydata3_carbon,

    }
    print(industries_list)

    # Second Graph, same as one but for waste
    years_list_carbon_waste = WasteIndustry.objects.all().values_list('year', flat=True).distinct().order_by('year')
    print(years_list_carbon_waste)
    industries_list_waste = WasteIndustry.objects.all().values_list('industry', flat=True).distinct()
    intensities_list_waste = []
    intensities_list2_waste = []
    intensities_list3_waste = []
    for x in WasteIndustry.objects.filter(industry="Water industry").values_list('total_amount', flat=True):
        y = json.dumps(x, cls=DjangoJSONEncoder)
        intensities_list_waste.append(float(x) / 1000)

    for x in WasteIndustry.objects.filter(industry="Power industry").values_list('total_amount', flat=True):
        y = json.dumps(x, cls=DjangoJSONEncoder)
        intensities_list2_waste.append(float(x) / 1000)

    for x in WasteIndustry.objects.filter(industry="Agriculture, forestry and fishing").values_list('total_amount',
                                                                                                    flat=True):
        y = json.dumps(x, cls=DjangoJSONEncoder)
        intensities_list3_waste.append(float(x) / 1000)

    xdata_waste = years_list_carbon_waste
    ydata_waste = intensities_list_waste
    ydata2_waste = intensities_list2_waste
    ydata3_waste = intensities_list3_waste
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}
    chartdata_waste = {
        'x': xdata_waste,
        'name1': 'Water industry', 'y1': ydata_waste, 'extra1': extra_serie,
        'name2': 'Power industry', 'y2': ydata2_waste, 'extra2': extra_serie,
        'name3': 'Agriculture, forestry and fishing', 'y3': ydata3_waste, 'extra3': extra_serie,
    }

    # Third Graph, pie chart for now
    xdata_water = WaterIndustry.objects.all().values_list('industry', flat=True)
    intensities_list_water = []
    for x in WaterIndustry.objects.all().values_list('amount', flat=True):
        y = json.dumps(x, cls=DjangoJSONEncoder)
        intensities_list_water.append(json.loads(y))
    ydata_water = intensities_list_water
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " Units"}
    }
    chartdata_water = {
        'x': xdata_water,
        'name1': 'series 1', 'y1': ydata_water, 'extra1': extra_serie,
    }
    charttype_carbon = "lineChart"
    chartcontainer_carbon = 'linechart_container_carbon'  # container name
    charttype_water = "pieChart"
    chartcontainer_water = 'piechart_container_water'  # container name
    charttype_waste = "lineChart"
    chartcontainer_waste = 'linechart_container_waste'  # container name
    # pass all graphs and their relevant data to the template at once
    user_details = UserDetails.objects.get(user_id=request.user.id)
    com_name = user_details.company_name
    data = {
        'charttype_carbon': charttype_carbon,
        'chartdata_carbon': chartdata_carbon,
        'chartcontainer_carbon': chartcontainer_carbon,
        'charttype_water': charttype_water,
        'chartdata_water': chartdata_water,
        'chartcontainer_water': chartcontainer_water,
        'charttype_waste': charttype_waste,
        'chartdata_waste': chartdata_waste,
        'chartcontainer_waste': chartcontainer_waste,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'company': com_name
    }


    return render(request, 'generic_dashboard.html', data)
