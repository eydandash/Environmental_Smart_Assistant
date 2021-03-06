# Generated by Django 3.0.3 on 2020-04-07 18:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0024_auto_20200407_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carboncompany',
            name='reporting_period',
        ),
        migrations.AlterField(
            model_name='carbonindustry',
            name='industry_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='no_of_employees',
            field=models.IntegerField(blank=True, default=15, null=True),
        ),
    ]
