# Generated by Django 3.0.3 on 2020-04-08 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0035_auto_20200407_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carboncompany',
            name='scope',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=12, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='watercompany',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=28, editable=False, null=True),
        ),
    ]
