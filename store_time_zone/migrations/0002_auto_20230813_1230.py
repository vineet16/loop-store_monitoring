# Generated by Django 4.2.4 on 2023-08-13 12:30

from django.db import migrations
from django.conf import settings
import csv
import os

def store_timezone_csv(apps, schema_editor):
    obj = apps.get_model('store_time_zone', 'Store')
    with open(os.path.join(settings.CSV_PATH, 'timezone.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            obj.objects.create(
                store_id=row['store_id'],
                timezone_str=row['timezone_str'],
            )

class Migration(migrations.Migration):

    dependencies = [
        ('store_time_zone', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(store_timezone_csv,reverse_code=migrations.RunPython.noop)
    ]