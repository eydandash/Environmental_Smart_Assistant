# Generated by Django 3.0.3 on 2020-04-03 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0008_auto_20200401_2007'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]