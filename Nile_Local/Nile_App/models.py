import uuid
from random import randint

from django.db import models
from django.contrib.auth.models import User


class CarbonCompany(models.Model):
    company_id = models.CharField(primary_key=True, max_length=50)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    total_emissions = models.IntegerField(blank=True, null=True)
    reporting_period = models.DateField(blank=True, null=True)
    scope = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Carbon_Company'


class CarbonIndustry(models.Model):
    year = models.IntegerField()
    industry = models.CharField(max_length=255)
    intensity = models.DecimalField(max_digits=65535, decimal_places=65535)
    industry_id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'Carbon_Industry'


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    industry = models.CharField(max_length=50, blank=True, null=True)
    company_address = models.CharField(max_length=255)
    company_no = models.CharField(max_length=30, blank=True, null=True)
    joining_date = models.DateField()
    email = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=30, blank=True, null=True)
    no_of_employees = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)
    company_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Users'


class WasteCompany(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'Waste_Company'


class WasteIndustry(models.Model):
    year = models.IntegerField()
    industry = models.CharField(max_length=100)
    total_amount = models.CharField(max_length=50)
    country = models.CharField(db_column='Country', max_length=25, blank=True, null=True)  # Field name made lowercase.
    industry_id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'Waste_Industry'


class WaterCompany(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=50)
    customer_name = models.CharField(max_length=50)
    industry = models.CharField(max_length=50, blank=True, null=True)
    reporting_period = models.CharField(max_length=255)
    bill_amount = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Water_Company'


class WaterIndustry(models.Model):
    year = models.IntegerField()
    industry = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535)
    provider = models.CharField(max_length=100, blank=True, null=True)
    industry_id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'Water_Industry'


# Create your models here.
class UserDetails(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want, blank != null, null is DB related while blank is form-related
    industry = models.CharField(max_length=50, blank=True, null=True)
    company_address = models.CharField(max_length=255, null=True)
    contact_no = models.CharField(max_length=30, blank=True, null=True)
    no_of_employees = models.IntegerField(blank=True, null=True, default=randint(10, 30))
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
