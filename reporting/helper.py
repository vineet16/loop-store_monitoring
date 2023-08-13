import tempfile
from pytz import timezone as pytz_timezone
from store_polling_status.models import PollingLogs, PollingStatus
from store_time_zone.models import Store
import datetime
import csv
import os
from .backgroundTask import Status

def generateReport(input : str, task_progress):

    task_progress.set( Status.STARTED, progress_message="The report generation has been started" )
    
    storeData = Store.objects.all()
    csv_data = []
    i = 1
    
    for store in storeData:

        tz = store.timezone_str or 'America/Chicago'
        target_timezone = pytz_timezone(tz)

        max_time = store.polling_status.order_by('-timestamp').first()
        if not max_time:
            continue
        max_time = max_time.timestamp
        local_time = max_time.astimezone(target_timezone)
        utc_timezone = pytz_timezone('UTC')
        utc_time = max_time.astimezone(utc_timezone)
        current_day = local_time.weekday()
        current_time = local_time.time()

        # last one hour 
        last_one_hour_data = get_last_one_hour_data(store, utc_time, current_day, current_time)
        # last one day
        last_one_day_data = get_last_one_day_data(store, utc_time, current_day, current_time)

        # last one week
        last_one_week_data = get_last_one_week_data(store, utc_time, current_day, current_time)
        data = []
        data.append(store.pk)
        data.extend(list(last_one_hour_data.values()))
        data.extend(list(last_one_day_data.values()))
        data.extend(list(last_one_week_data.values()))
        csv_data.append(data)
        
        task_progress.set( Status.RUNNING, progress_message=f"{ i / storeData.count() }% has been processed" )
        i = i+1
    
    file_name = "final_report.csv"
    temp_file_path = ""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, file_name)
        with open(temp_file_path, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["store_id", "uptime_last_hour", "uptime_last_day", "update_last_week", "downtime_last_hour", "downtime_last_day", "downtime_last_week"])
            for data in csv_data:
                csv_writer.writerow(data)

    task_progress.set( Status.SUCCESS, output=temp_file_path )


def get_last_one_hour_data(store, utc_time, current_day, current_time):
    last_one_hour_data = {"uptime" : 0 , "downtime" : 0 , "unit" : "minutes"}
    is_store_open = store.business_hours.filter(day=current_day,start_time__lte=current_time,end_time__gte=current_time).exists()
    if not is_store_open:
        return last_one_hour_data
    last_one_hour_logs = store.polling_status.filter(timestamp__gte=utc_time - datetime.timedelta(hours=1)).order_by('timestamp')
    if last_one_hour_logs:
        last_one_hour_log_status = last_one_hour_logs[0].status
        if last_one_hour_log_status == PollingStatus.ACTIVE:
            last_one_hour_data["uptime"] = 60
        else:
            last_one_hour_data["downtime"] = 60

    return last_one_hour_data
    

def get_last_one_day_data(store, utc_time, current_day, current_time):
    last_one_day_data = {"uptime" : 0 , "downtime" : 0, "unit" : "hours"}
    one_day_ago = current_day - 1 if current_day > 0 else 6
    is_store_open = store.business_hours.filter(day__gte=one_day_ago,day__lte=current_day,start_time__lte=current_time,end_time__gte=current_time).exists()
    if not is_store_open:
        return last_one_day_data
    last_one_day_logs = store.polling_status.filter(timestamp__gte=utc_time - datetime.timedelta(days=1)).order_by('timestamp')
    for log in last_one_day_logs:
        log_in_store_business_hours = store.business_hours.filter(
            day=log.timestamp.weekday(),
            start_time__lte=log.timestamp.time(),
            end_time__gte=log.timestamp.time()
            ).exists()
        if not log_in_store_business_hours:
            continue
        if log.status == PollingStatus.ACTIVE:
            last_one_day_data["uptime"] += 1
        else:
            last_one_day_data["downtime"] += 1
    return last_one_day_data

def get_last_one_week_data(store, utc_time, current_day, current_time):
    last_one_week_data = {"uptime" : 0 , "downtime" : 0, "unit" : "hours"}
    one_week_ago = current_day - 7 if current_day > 0 else 0
    is_store_open = store.business_hours.filter(day__gte=one_week_ago,day__lte=current_day,start_time__lte=current_time,end_time__gte=current_time).exists()
    if not is_store_open:
        return last_one_week_data
    last_one_week_logs = store.polling_status.filter(timestamp__gte=utc_time - datetime.timedelta(days=7)).order_by('timestamp')
    for log in last_one_week_logs:
        log_in_store_business_hours = store.business_hours.filter(
            day=log.timestamp.weekday(),
            start_time__lte=log.timestamp.time(),
            end_time__gte=log.timestamp.time()
            ).exists()
        if not log_in_store_business_hours:
            continue
        if log.status == PollingStatus.ACTIVE:
            last_one_week_data["uptime"] += 1
        else:
            last_one_week_data["downtime"] += 1
    
    return last_one_week_data