# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(CarbonCompany)
admin.site.register(WaterCompany)
admin.site.register(WasteCompany)

