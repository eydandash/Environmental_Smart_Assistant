# Generated by Django 3.0.3 on 2020-04-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0012_auto_20200405_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=17, null=True),
        ),
    ]
