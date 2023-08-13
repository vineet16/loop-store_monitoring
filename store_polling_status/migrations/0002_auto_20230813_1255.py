# Generated by Django 4.2.4 on 2023-08-13 12:55

from dateutil import parser
import pytz
from django.db import migrations
from store_polling_status.models import PollingStatus
from django.conf import settings
import csv
import os

def store_store_status_csv(apps, schema_editor):
    Store = apps.get_model('store_time_zone', 'Store')
    PollingLogs = apps.get_model('store_polling_status', 'PollingLogs')
    with open(os.path.join(settings.CSV_PATH, 'store_status.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            store = Store.objects.filter(store_id=row['store_id']).first()
            status = PollingStatus.ACTIVE if row['status'] == 'active' else PollingStatus.INACTIVE
            csv_datetime = row['timestamp_utc'][:len(row['timestamp_utc'])-4]
            unaware_time = parser.parse(csv_datetime)
            timestamp = unaware_time.replace(tzinfo=pytz.UTC)
            if store:
                PollingLogs.objects.create(
                    store=store,
                    status=status,
                    timestamp=timestamp
                )

class Migration(migrations.Migration):

    dependencies = [
        ('store_polling_status', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(store_store_status_csv, reverse_code=migrations.RunPython.noop),
    ]
