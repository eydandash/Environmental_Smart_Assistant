from django.shortcuts import render
from Nile_App.models import CarbonIndustry, WaterIndustry, WasteIndustry, UserDetails
import json
from django.core.serializers.json import DjangoJSONEncoder


def dashboard(request):
    # First GRAPH, to compare carbon_intensity per industry per year LINE CHART,
    years_list_carbon = CarbonIndustry.objects.all().values_list('year', flat=True).distinct().order_by('year')
    industries_list_carbon = CarbonIndustry.objects.all().order_by('year')
    list_ind = set([e.industry for e in industries_list_carbon])
    intensities_list = []
    i=1
    xdata_carbon = years_list_carbon
    chartdata_carbon = {
        'x': xdata_carbon,
    }
    # Loop through all industries, then for every industry, create a list of intensities across different years,
    # and pass that list straight into the NVD3 parameter list for the chart. Empty the intensities list then
    # increment the  counter i which is used only to be able to use name1, name2, name3, etc (how NVD3 reads dict
    # values). The serializer is used to to convert Decimal types into any JSON identifiable format.
    for ind in list_ind:
        for x in CarbonIndustry.objects.filter(industry=ind).values_list('intensity', flat=True):
            y = json.dumps(x, cls=DjangoJSONEncoder)
            intensities_list.append(json.loads(y))
        chartdata_carbon.update({'name' + str(i): ind, 'y' + str(i): intensities_list})
        intensities_list = []
        i+=1

    # Second Graph, same as carbon but for waste
    years_list_waste = WasteIndustry.objects.all().values_list('year', flat=True).distinct().order_by('year')
    industries_list_waste = WasteIndustry.objects.all()
    list_ind = set([e.industry for e in industries_list_waste])
    temp_waste_amounts = []
    i = 0
    xdata_waste = years_list_waste
    chartdata_waste = {
        'x': xdata_waste
    }
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " Tonnes"}
    }
    for ind in list_ind:
        for x in WasteIndustry.objects.filter(industry=ind).values_list('total_amount', flat=True):
            y = json.dumps(x, cls=DjangoJSONEncoder)
            temp_waste_amounts.append(float(x) / 1000)
        chartdata_waste.update({'name' + str(i): ind, 'y' + str(i): temp_waste_amounts, 'extra' + str(i): extra_serie1})
        temp_waste_amounts = []
        i+=1


    # intensities_list_waste = []
    # intensities_list2_waste = []
    # intensities_list3_waste = []
    # for x in WasteIndustry.objects.filter(industry="Water industry").values_list('total_amount', flat=True):
    #     y = json.dumps(x, cls=DjangoJSONEncoder)
    #     intensities_list_waste.append(float(x) / 1000)
    #
    # for x in WasteIndustry.objects.filter(industry="Power industry").values_list('total_amount', flat=True):
    #     y = json.dumps(x, cls=DjangoJSONEncoder)
    #     intensities_list2_waste.append(float(x) / 1000)
    #
    # for x in WasteIndustry.objects.filter(industry="Agriculture, forestry and fishing").values_list('total_amount',
    #                                                                                                 flat=True):
    #     y = json.dumps(x, cls=DjangoJSONEncoder)
    #     intensities_list3_waste.append(float(x) / 1000)
    #
    # xdata_waste = years_list_waste
    # ydata_waste = intensities_list_waste
    # ydata2_waste = intensities_list2_waste
    # ydata3_waste = intensities_list3_waste
    # extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}
    # chartdata_waste = {
    #     'x': xdata_waste,
    #     'name1': 'Water industry', 'y1': ydata_waste, 'extra1': extra_serie,
    #     'name2': 'Power industry', 'y2': ydata2_waste, 'extra2': extra_serie,
    #     'name3': 'Agriculture, forestry and fishing', 'y3': ydata3_waste, 'extra3': extra_serie,
    # }
    # Third Graph, pie chart for water since only data for one year is available.
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

    # pass all graphs and their relevant data to the template at once, a better practice is updating dict once at a
    # time as followed in the other three specific dashboard views code.
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
        'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'company': com_name
    }

    return render(request, 'generic_dashboard.html', data)
