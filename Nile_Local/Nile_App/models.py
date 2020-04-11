import uuid
from random import randint
from django.db import models
from django.contrib.auth.models import User


class CarbonCompany(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    total_emissions = models.DecimalField(max_digits=500, decimal_places=2, null=True)
    scope = models.IntegerField(null=True)
    year = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'Carbon_Company'


class CarbonIndustry(models.Model):
    industry_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField()
    industry = models.CharField(max_length=255)
    intensity = models.DecimalField(max_digits=65535, decimal_places=65535)


    class Meta:
        managed = True
        db_table = 'Carbon_Industry'


class WasteCompany(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    company_name = models.CharField(max_length=50, null=True)
    amount = models.DecimalField(max_digits=500, decimal_places=2, null=True)
    year = models.IntegerField(null=True)
    type = models.CharField(max_length=100, null=True)
    industry = models.CharField(max_length=100, null=True)

    class Meta:
        managed = True
        db_table = 'Waste_Company'


class WasteIndustry(models.Model):
    year = models.IntegerField()
    industry = models.CharField(max_length=100)
    total_amount = models.CharField(max_length=50)
    country = models.CharField(db_column='Country', max_length=25, blank=True, null=True)  # Field name made lowercase.
    industry_id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'Waste_Industry'


class WaterCompany(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    company_name = models.CharField(max_length=50)
    industry = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField()
    no_of_employees = models.IntegerField(blank=True, null=True, default=randint(10, 30), editable=False)
    supplier = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Water_Company'


class WaterIndustry(models.Model):
    year = models.IntegerField()
    industry = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535)
    provider = models.CharField(max_length=100, blank=True, null=True)
    industry_id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'Water_Industry'


# Create your models here.
class UserDetails(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want, blank != null, null is DB related while blank is form-related
    industry = models.CharField(max_length=50, blank=True, null=True)
    company_address = models.CharField(max_length=255, null=True)
    contact_no = models.CharField(max_length=30, blank=True, null=True)
    no_of_employees = models.IntegerField(blank=True, null=True, default=randint(10, 30), editable=False)
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
