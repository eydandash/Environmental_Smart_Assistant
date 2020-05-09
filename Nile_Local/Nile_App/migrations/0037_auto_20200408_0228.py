# Generated by Django 3.0.3 on 2020-04-08 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0036_auto_20200408_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carboncompany',
            name='total_emissions',
            field=models.DecimalField(decimal_places=2, max_digits=500, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=20, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='watercompany',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=18, editable=False, null=True),
        ),
    ]