# Generated by Django 3.0.3 on 2020-04-01 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0007_auto_20200401_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='joining_date',
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=23, null=True),
        ),
    ]
