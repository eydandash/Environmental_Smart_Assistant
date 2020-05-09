# This file contains all extra preprocessing and calculations that are performed on the data displayed ina nay of the
# 4 dashboard templates

# Calculating total Carbon cost, https://qz.com/1192753/a-carbon-tax-killed-coal-in-the-uk-natural-gas-is-next/
from _decimal import Decimal
from typing import Dict


def get_carbon_cost(tonnes):
    # Using decimal here is important to since multiplication by decimals sabotages precision and produces wrong long results
    return 18 * Decimal(tonnes)


# Calculating the total water usage, based on the number of employees * 50 litres(m3) * 5 days work * 52 weeks, then divided by 10^12 for ease of presentation
# found here https://www.south-staffs-water.co.uk/media/1509/waterusebusiness.pdf
# Note that the if condition was since small emp values lead to presision issues that made cost for all entries = zerp on thirs graph

def get_water_consum(emp):
    if emp > 1000:
        return emp * emp * 5 * 52 / 100000000000
    return emp * emp * 5 * 52

# Calculating the water cost, depending the supplier, there is no need to classify into business size because the m3
# price is still the same, found here https://www.businesselectricityprices.org.uk/water-prices/

providers = {
    'Thames Water': 1.3560,
    'Severn Trent': 1.5586,
    'United Utilities': 1.7050,
    'Northumbrian': 1.2195,
    'Yorkshire Water': 1.2875,
    'Anglian Water': 1.3396,
    'Southern Water': 1.2510,
    'Wessex Water': 2.2058,
    'South West': 1.9714,
    'Business Stream': 2.1442
}


def get_water_cost(emp, supp):
    consum = get_water_consum(emp)
    current_rate = providers.get(supp)
    cost = (consum * current_rate)
    cost = format(cost, '.2f') # Just formating to 2 decimal places for presentation
    recommended_supp = {}
    for key, value in providers.items():
        if current_rate > value:
            recommended_supp.update({key: value})
            # returns a tuple
    return cost, recommended_supp


# Calculating the waste cost. found here https://startuptoday.co.uk/business-1/how-much-waste-is-produced-in-the-uk/


def get_waste_cost(tonnes):
    return 3500 * tonnes /1000000 #dividing by a million for presentation