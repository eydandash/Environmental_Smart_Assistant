# Generated by Django 3.0.3 on 2020-04-01 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0005_auto_20200401_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='joining_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
