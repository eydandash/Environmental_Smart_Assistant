# Generated by Django 3.0.3 on 2020-04-01 19:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Nile_App', '0006_auto_20200401_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='company_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]