import datetime
import random
import time

from django.shortcuts import render
from django.http import request
from Nile_App.models import CarbonIndustry
from nvd3 import pieChart
import json
from django.core.serializers.json import DjangoJSONEncoder
def dashboard(request):

    # First GRAPH, to compare carbon_intensity per industry per year LINE CHART, Since maps are not subscriptable, I had to format all of the maps which return a map
    # to a list to use the, in graphs. Using maps as included in the official NVD3 Django documentation didn't work.
    # PLEASE NOTE: ind = industry, y = year, ci = carbon intensity
    # The serializer and deserializer, keep failing to convert Decimal types into any JSON identifiable format.
    years_list = CarbonIndustry.objects.all().values_list('year', flat=True).distinct().order_by('year')
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
    xdata = years_list
    ydata = intensities_list
    ydata2 = intensities_list2
    ydata3 = intensities_list3
    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " calls"},
                    "date_format": tooltip_date}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " min"},
                    "date_format": tooltip_date}

    chartdata = {
        'x': xdata,
        'name1': 'Manufacturing', 'y1': ydata, 'extra1': extra_serie1,
        'name2': 'Transport and Storage', 'y2': ydata2, 'extra2': extra_serie1,
        'name3': 'Construction', 'y3': ydata3, 'extra3': extra_serie1

    }
    print(industries_list)
    # Second Graph, pie chart for now
    xdata1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    ydata1 = [3, 5, 7, 8, 3, 5, 3, 5, 7, 6, 3, 1]
    extra_serie = {}
    chartdata1 = {
        'x': xdata1,
        'name1': 'series 1', 'y1': ydata1, 'extra1': extra_serie,
    }
    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    charttype1 = "pieChart"
    chartcontainer1 = 'piechart_container1'  # container name

    # pass all graphs and their relevant data to the template at once
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'charttype1': charttype1,
        'chartdata1': chartdata1,
        'chartcontainer1': chartcontainer1,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
        'extra1': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render(request, 'generic_dashboard.html', data)

